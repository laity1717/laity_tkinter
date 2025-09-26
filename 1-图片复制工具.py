# -*- coding: utf-8 -*-  python 3.12
# @Time    : 2025/9/10
# @Desc    : 图片复制工具
# @Author  : laity
# @Contact : 微信公众号：laity的渗透测试之路


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from pathlib import Path
import threading


class ImageCopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片复制工具")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # 支持的图片格式
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

        self.setup_ui()

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 源文件夹选择
        ttk.Label(main_frame, text="源文件夹:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.source_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.source_var, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="浏览...", command=self.browse_source).grid(row=0, column=2)

        # 目标文件夹选择
        ttk.Label(main_frame, text="目标文件夹:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dest_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.dest_var, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(main_frame, text="浏览...", command=self.browse_dest).grid(row=1, column=2)

        # 选项框架
        options_frame = ttk.LabelFrame(main_frame, text="选项", padding="5")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        self.keep_structure = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="保持文件夹结构", variable=self.keep_structure).grid(row=0, column=0,
                                                                                                 sticky=tk.W)

        self.overwrite = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="覆盖已存在文件", variable=self.overwrite).grid(row=0, column=1,
                                                                                            sticky=tk.W, padx=20)

        # 进度条
        ttk.Label(main_frame, text="进度:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=5)

        # 日志文本框
        ttk.Label(main_frame, text="操作日志:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.log_text = tk.Text(main_frame, height=10, width=70)
        self.log_text.grid(row=6, column=0, columnspan=3, pady=5)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="开始复制", command=self.start_copy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空日志", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="退出", command=self.root.quit).pack(side=tk.LEFT, padx=5)

        # 配置网格权重
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def browse_source(self):
        folder = filedialog.askdirectory(title="选择源文件夹")
        if folder:
            self.source_var.set(folder)

    def browse_dest(self):
        folder = filedialog.askdirectory(title="选择目标文件夹")
        if folder:
            self.dest_var.set(folder)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def start_copy(self):
        source = self.source_var.get()
        dest = self.dest_var.get()

        if not source or not dest:
            messagebox.showerror("错误", "请选择源文件夹和目标文件夹")
            return

        if source == dest:
            messagebox.showerror("错误", "源文件夹和目标文件夹不能相同")
            return

        # 在后台线程中执行复制操作
        thread = threading.Thread(target=self.copy_images, args=(source, dest))
        thread.daemon = True
        thread.start()

    def copy_images(self, source, dest):
        self.progress.start()
        self.status_var.set("正在复制图片...")

        try:
            total_copied = 0
            source_path = Path(source)
            dest_path = Path(dest)

            # 遍历所有文件
            for file_path in source_path.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in self.image_extensions:
                    relative_path = file_path.relative_to(source_path)

                    if self.keep_structure.get():
                        # 保持文件夹结构
                        target_path = dest_path / relative_path
                        target_dir = target_path.parent
                    else:
                        # 不保持文件夹结构，所有文件放在同一目录
                        target_path = dest_path / file_path.name
                        target_dir = dest_path

                    # 确保目标目录存在
                    target_dir.mkdir(parents=True, exist_ok=True)

                    # 检查文件是否已存在
                    if target_path.exists() and not self.overwrite.get():
                        self.log_message(f"跳过已存在文件: {relative_path}")
                        continue

                    # 复制文件
                    shutil.copy2(file_path, target_path)
                    self.log_message(f"已复制: {relative_path}")
                    total_copied += 1

            self.status_var.set(f"完成! 共复制 {total_copied} 个图片文件")
            messagebox.showinfo("完成", f"图片复制完成! 共复制 {total_copied} 个文件")

        except Exception as e:
            self.status_var.set("复制过程中出现错误")
            self.log_message(f"错误: {str(e)}")
            messagebox.showerror("错误", f"复制过程中出现错误: {str(e)}")
        finally:
            self.progress.stop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCopyApp(root)
    root.mainloop()