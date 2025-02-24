import os
import glob

def hide_toctrees(rst_dir):
    print(rst_dir)
    for rst_file in glob.glob(os.path.join(rst_dir, "*.rst")):
        with open(rst_file, "r") as f:
            content = f.readlines()

        with open(rst_file, "w") as f:
            for line in content:
                if line.strip().startswith(".. toctree::"):
                    f.write(".. toctree::\n   :hidden:\n\n")  # Add :hidden: and extra newline
                else:
                    f.write(line)

if __name__ == "__main__":
    print(os.path.dirname(__file__))
    rst_directory = os.path.join(os.path.dirname(__file__), "source")
    print(rst_directory)
    hide_toctrees(rst_directory)
    print("Toctrees hidden in RST files.")