# Analysis reference

## Gait

### ```nimbalwear```
- Inputs: ankle-worn IMUs
- Event detection: step detection events (pushoff, early-swing, late-swing, heelstrike)
- Detector parameters:
    - pushoff_threshold: 0.85,
    - pushoff_time: 0.4,
    - swing_phase_time: 0.2,
    - heel_strike_detect_time: 0.5,
    - heel_strike_threshold: -5,
    - foot_down_time: 0.05
- Feature extraction metrics:
    - step_foot
    - step_start/end/duration
    - pushoff/early-swing/late-swing/heelstrike duration
    - maximum/average step acceleration
    
- Reference: [https://doi.org/10.1186/s44247-024-00062-3](https://doi.org/10.1186/s44247-024-00062-3)
```
@article{Beyer2024,
title = {NiMBaLWear analytics pipeline for wearable sensors: a modular,  open-source platform for evaluating multiple domains of health and behaviour},
volume = {2},
ISSN = {2731-684X},
url = {http://dx.doi.org/10.1186/s44247-024-00062-3},
DOI = {10.1186/s44247-024-00062-3},
number = {1},
journal = {BMC Digital Health},
publisher = {Springer Science and Business Media LLC},
author = {Beyer,  Kit B. and Weber,  Kyle S. and Cornish,  Benjamin F. and Vert,  Adam and Thai,  Vanessa and Godkin,  F. Elizabeth and McIlroy,  William E. and Van Ooteghem,  Karen},
year = {2024},
month = feb 
}
```

### ```paradigma```
- Inputs: wrist-worn IMUs
- Event detection: arm swing angle time series
- Detector parameters:
    - yz_columns = ["y", "z"]
- Feature extraction metrics:
    - peak arm swing velocity
    - arm swing amplitude
- Reference: [https://doi.org/10.1186/s12984-025-01578-z](https://doi.org/10.1186/s12984-025-01578-z)
```
@article{Post2025,
title = {Quantifying arm swing in Parkinson’s disease: a method accounting for arm activities during free-living gait},
volume = {22},
ISSN = {1743-0003},
url = {http://dx.doi.org/10.1186/s12984-025-01578-z},
DOI = {10.1186/s12984-025-01578-z},
number = {1},
journal = {Journal of NeuroEngineering and Rehabilitation},
publisher = {Springer Science and Business Media LLC},
author = {Post,  Erik and Laarhoven,  Twan van and Raykov,  Yordan P. and Little,  Max A. and Nonnekes,  Jorik and Heskes,  Tom M. and Bloem,  Bastiaan R. and Evers,  Luc J. W.},
year = {2025},
month = feb 
}
```

## ECG

### ```pan-tompkins```
- Inputs: ECG data
- Event detection: R-peak event times.
- Detector parameters:
    - ecg_channel: "ecg0"
- Feature extraction metrics:
    - HRV: Root mean square successive differences
    - HRV: SD R-R intervals (SDNN)
    - HRV: % of R-R intervals greater than 50ms (PNN50)
- Reference: [https://doi.org/10.1109/TBME.1985.325532](https://doi.org/10.1109/TBME.1985.325532)
```
@article{Pan1985,
  title = {A Real-Time QRS Detection Algorithm},
  volume = {BME-32},
  ISSN = {0018-9294},
  url = {http://dx.doi.org/10.1109/TBME.1985.325532},
  DOI = {10.1109/tbme.1985.325532},
  number = {3},
  journal = {IEEE Transactions on Biomedical Engineering},
  publisher = {Institute of Electrical and Electronics Engineers (IEEE)},
  author = {Pan,  Jiapu and Tompkins,  Willis J.},
  year = {1985},
  month = mar,
  pages = {230–236}
}
```