import subprocess
import time
import os

def run_program(path):
    # 使用绝对路径和适当的参数启动 Python 脚本
    return subprocess.Popen(["python3", path])

def main():
    # 程序路径和参数列表
    programs = [
        #    
            {
            "path": r"C:\Users\LingXiTong\Desktop\OCR4ZN-Hospital-main\OCR4ZN-Hospital-main\ZN-Hospital-WSIs-Rename.py",
        },  
                
    ]

    # 启动所有程序并保存进程对象
    processes = [run_program(prog['path']) for prog in programs]

    while True:
        for i, process in enumerate(processes):
            # 检查每个程序是否仍在运行
            if process.poll() is not None:  # 如果程序停止
                print(f"程序{i+1}已停止，重新启动...")
                prog = programs[i]
                processes[i] = run_program(prog['path']) # 重新启动程序
            else:
                print(f"程序{i+1}正在运行...")
                
        # 每隔40秒检查一次所有程序
        time.sleep(40)

if __name__ == "__main__":
    main()
    
    
