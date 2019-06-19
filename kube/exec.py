import subprocess

class EXEC:

    def exec_sh(self, cmd, print_enable=True):
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            if print_enable is True:
                print(output)
        except subprocess.CalledProcessError as err:
            print(err.output)
            raise
        return str(output.strip())
