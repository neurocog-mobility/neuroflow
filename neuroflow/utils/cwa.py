from openmovement.load.cwa_load import unpack, _checksum, _parse_timestamp, _timestamp_string, _dword_unpack

def parse_cwa_data(block, extractData=False):
    """(Slow) parser for a single block."""
    data = {}
    if len(block) >= 512:
        packetHeader = unpack(
            "BB", block[0:2]
        )  # @ 0  +2   ASCII "AX", little-endian (0x5841)
        packetLength = unpack("<H", block[2:4])[
            0
        ]  # @ 2  +2   Packet length (508 bytes, with header (4) = 512 bytes total)
        if (
            packetHeader[0] == ord("A")
            and packetHeader[1] == ord("X")
            and packetLength == 508
            and _checksum(block[0:512]) == 0
        ):
            # checksum = unpack('<H', block[510:512])[0]               # @510 +2   Checksum of packet (16-bit word-wise sum of the whole packet should be zero)

            deviceFractional = unpack("<H", block[4:6])[
                0
            ]  # @ 4  +2   Top bit set: 15-bit fraction of a second for the time stamp, the timestampOffset was already adjusted to minimize this assuming ideal sample rate; Top bit clear: 15-bit device identifier, 0 = unknown;
            data["deviceFractional"] = deviceFractional
            data["sessionId"] = unpack("<I", block[6:10])[
                0
            ]  # @ 6  +4   Unique session identifier, 0 = unknown
            data["sequenceId"] = unpack("<I", block[10:14])[
                0
            ]  # @10  +4   Sequence counter (0-indexed), each packet has a new number (reset if restarted)
            timestamp = _parse_timestamp(
                unpack("<I", block[14:18])[0]
            )  # @14  +4   Last reported RTC value, 0 = unknown
            light = unpack("<H", block[18:20])[
                0
            ]  # @18  +2   Lower 10 bits are the last recorded light sensor value in raw units, 0 = none #  log10LuxTimes10Power3 = ((value + 512.0) * 6000 / 1024); lux = pow(10.0, log10LuxTimes10Power3 / 1000.0);
            data["light"] = light & 0x3FF  # least-significant 10 bits
            temperature = unpack("<H", block[20:22])[
                0
            ]  # @20  +2   Last recorded temperature sensor value in raw units, 0 = none
            data["temperature"] = temperature * 75.0 / 256 - 50
            data["events"] = unpack("B", block[22:23])[
                0
            ]  # @22  +1   Event flags since last packet, b0 = resume logging, b1 = reserved for single-tap event, b2 = reserved for double-tap event, b3 = reserved, b4 = reserved for diagnostic hardware buffer, b5 = reserved for diagnostic software buffer, b6 = reserved for diagnostic internal flag, b7 = reserved)
            battery = unpack("B", block[23:24])[
                0
            ]  # @23  +1   Last recorded battery level in raw units, 0 = unknown
            data["battery"] = (battery + 512.0) * 6000 / 1024 / 1000.0
            rateCode = unpack("B", block[24:25])[
                0
            ]  # @24  +1   Sample rate code, frequency (3200/(1<<(15-(rate & 0x0f)))) Hz, range (+/-g) (16 >> (rate >> 6)).
            data["rateCode"] = rateCode
            numAxesBPS = unpack("B", block[25:26])[
                0
            ]  # @25  +1   0x32 (top nibble: number of axes = 3; bottom nibble: packing format - 2 = 3x 16-bit signed, 0 = 3x 10-bit signed + 2-bit exponent)
            data["numAxesBPS"] = numAxesBPS
            timestampOffset = unpack("<h", block[26:28])[
                0
            ]  # @26  +2   Relative sample index from the start of the buffer where the whole-second timestamp is valid
            data["sampleCount"] = unpack("<H", block[28:30])[
                0
            ]  # @28  +2   Number of accelerometer samples (40/80/120, depending on format, if this sector is full)
            # rawSampleData[480] = block[30:510]                      # @30  +480 Raw sample data.  Each sample is either 3x 16-bit signed values (x, y, z) or one 32-bit packed value (The bits in bytes [3][2][1][0]: eezzzzzz zzzzyyyy yyyyyyxx xxxxxxxx, e = binary exponent, lsb on right)

            # range = 16 >> (rateCode >> 6)  ## Nearest configured frequency: 3200 / (2 ^ round(log2(3200 / frequency)))
            if (
                rateCode == 0x00
            ):  # Very old format used timestampOffset to indicate sample rate
                frequency = timestampOffset
            else:
                frequency = 3200 / (1 << (15 - (rateCode & 0x0F)))
            data["frequency"] = frequency

            timeFractional = 0
            # if top-bit set, we have a fractional date
            if deviceFractional & 0x8000:
                # Need to undo backwards-compatible shim by calculating how many whole samples the fractional part of timestamp accounts for.
                timeFractional = (
                    deviceFractional & 0x7FFF
                ) << 1  # use original deviceId field bottom 15-bits as 16-bit fractional time
                timestampOffset += (
                    timeFractional * int(frequency)
                ) >> 16  # undo the backwards-compatible shift (as we have a true fractional)

            # Add fractional time to timestamp
            timestamp += timeFractional / 65536

            data["timestamp"] = timestamp
            data["timestampOffset"] = timestampOffset

            data["timestampTime"] = _timestamp_string(data["timestamp"])

            # Maximum samples per sector
            channels = (numAxesBPS >> 4) & 0x0F
            bytesPerAxis = numAxesBPS & 0x0F
            bytesPerSample = 4
            if bytesPerAxis == 0 and channels == 3:
                bytesPerSample = 4
            elif bytesPerAxis > 0 and channels > 0:
                bytesPerSample = bytesPerAxis * channels
            samplesPerSector = 480 // bytesPerSample
            data["channels"] = channels
            data["bytesPerAxis"] = bytesPerAxis  # 0 for DWORD packing
            data["bytesPerSample"] = bytesPerSample
            data["samplesPerSector"] = samplesPerSector

            # Estimate the time of the first/after-last sample (if at the configured rate)
            data["estimatedFirstSampleTime"] = timestamp - (timestampOffset / frequency)
            data["estimatedAfterLastSampleTime"] = data["estimatedFirstSampleTime"] + (
                samplesPerSector / frequency
            )

            # Axes
            accelAxis = -1
            gyroAxis = -1
            magAxis = -1
            if channels >= 6:
                gyroAxis = 0
                accelAxis = 3
                if channels >= 9:
                    magAxis = 6
            elif channels >= 3:
                accelAxis = 0

            # Default units/scaling/range
            accelUnit = 256  # 1g = 256
            gyroRange = 2000  # 32768 = 2000dps
            magUnit = 16  # 1uT = 16
            # light is least significant 10 bits, accel scale 3-MSB, gyro scale next 3 bits: AAAGGGLLLLLLLLLL
            accelUnit = 1 << (8 + ((light >> 13) & 0x07))
            if ((light >> 10) & 0x07) != 0:
                gyroRange = 8000 // (1 << ((light >> 10) & 0x07))

            # Scale
            # accelScale = 1.0 / accelUnit
            # gyroScale = float(gyroRange) / 32768
            # magScale = 1.0 / magUnit

            # Range
            accelRange = 16
            if rateCode != 0:
                accelRange = 16 >> (rateCode >> 6)
            magRange = 32768 / magUnit

            # Unit
            gyroUnit = 32768.0 / gyroRange

            if accelAxis >= 0:
                data["accelAxis"] = accelAxis
                data["accelRange"] = accelRange
                data["accelUnit"] = accelUnit
            if gyroAxis >= 0:
                data["gyroAxis"] = gyroAxis
                data["gyroRange"] = gyroRange
                data["gyroUnit"] = gyroUnit
            if magAxis >= 0:
                data["magAxis"] = magAxis
                data["magRange"] = magRange
                data["magUnit"] = magUnit

            # Read sample values
            if extractData:
                if accelAxis >= 0:
                    # accelSamples = [[0, 0, 0]] * data["sampleCount"]
                    accelSamples = [[0, 0, 0] for _ in range(data['sampleCount'])]
                    if bytesPerAxis == 0 and channels == 3:
                        for i in range(data["sampleCount"]):
                            ofs = 30 + i * 4
                            # value =  block[i] | (block[i + 1] << 8) | (block[i + 2] << 16) | (block[i + 3] << 24)
                            value = unpack("<I", block[ofs : ofs + 4])[0]
                            axes = _dword_unpack(value)
                            accelSamples[i][0] = axes[0] / accelUnit
                            accelSamples[i][1] = axes[1] / accelUnit
                            accelSamples[i][2] = axes[2] / accelUnit
                    elif bytesPerAxis == 2:
                        for i in range(data["sampleCount"]):
                            ofs = 30 + (i * 2 * channels) + 2 * accelAxis
                            accelSamples[i][0] = (
                                block[ofs + 0] | (block[ofs + 1] << 8)
                            ) / accelUnit
                            accelSamples[i][1] = (
                                block[ofs + 2] | (block[ofs + 3] << 8)
                            ) / accelUnit
                            accelSamples[i][2] = (
                                block[ofs + 4] | (block[ofs + 5] << 8)
                            ) / accelUnit
                    data["samplesAccel"] = accelSamples

                if gyroAxis >= 0 and bytesPerAxis == 2:
                    # gyroSamples = [[0, 0, 0]] * data["sampleCount"]
                    gyroSamples = [[0, 0, 0] for _ in range(data['sampleCount'])]
                    for i in range(data["sampleCount"]):
                        ofs = 30 + (i * 2 * channels) + 2 * gyroAxis
                        gyroSamples[i][0] = (
                            block[ofs + 0] | (block[ofs + 1] << 8)
                        ) / gyroUnit
                        gyroSamples[i][1] = (
                            block[ofs + 2] | (block[ofs + 3] << 8)
                        ) / gyroUnit
                        gyroSamples[i][2] = (
                            block[ofs + 4] | (block[ofs + 5] << 8)
                        ) / gyroUnit
                    data["samplesGyro"] = gyroSamples

                if magAxis >= 0 and bytesPerAxis == 2:
                    magSamples = [[0, 0, 0]] * data["sampleCount"]
                    for i in range(data["sampleCount"]):
                        ofs = 30 + (i * 2 * channels) + 2 * magAxis
                        magSamples[i][0] = (
                            block[ofs + 0] | (block[ofs + 1] << 8)
                        ) / magUnit
                        magSamples[i][1] = (
                            block[ofs + 2] | (block[ofs + 3] << 8)
                        ) / magUnit
                        magSamples[i][2] = (
                            block[ofs + 4] | (block[ofs + 5] << 8)
                        ) / magUnit
                    data["samplesMag"] = magSamples

    return data
