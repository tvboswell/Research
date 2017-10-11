import subprocess
def compile_java(java_file):
    cmd = 'javac ' + java_file 
    proc = subprocess.Popen(cmd, shell=True)

compile_java("HelloWorld.java")
