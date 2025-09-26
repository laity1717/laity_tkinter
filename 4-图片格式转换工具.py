# -*- coding: utf-8 -*-  python 3.12
# @Time    : 2025/9/10
# @Desc    : 图片格式转换工具
# @Author  : laity
# @Contact : 微信公众号：laity的渗透测试之路


from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class ImageConverterApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("批量图片格式转换工具")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 设置背景图
        self.setup_background()
        
        # 初始化UI组件
        self.setup_ui()
    
    def setup_background(self):
        try:
            # 尝试加载背景图片
            self.bg_image = tk.PhotoImage(file="img/bg.png")
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            # 如果加载背景图失败，使用纯色背景
            print(f"无法加载背景图片: {e}")
            self.root.configure(bg="#f0f0f0")
    
    def setup_ui(self):
        # 创建主框架
        main_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.RAISED)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=300)
        
        # 标题
        title_label = tk.Label(main_frame, text="批量图片格式转换", 
                              font=("Arial", 16, "bold"), bg="white")
        title_label.pack(pady=10)
        
        # 输入文件夹
        input_frame = tk.Frame(main_frame, bg="white")
        input_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(input_frame, text="输入文件夹:", bg="white").pack(side=tk.LEFT)
        self.entry_input = tk.Entry(input_frame, width=30)
        self.entry_input.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        tk.Button(input_frame, text="浏览", bg="#4CAF50", fg="white",
                  command=lambda: self.select_folder(self.entry_input)).pack(side=tk.LEFT)
        
        # 输出文件夹
        output_frame = tk.Frame(main_frame, bg="white")
        output_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(output_frame, text="输出文件夹:", bg="white").pack(side=tk.LEFT)
        self.entry_output = tk.Entry(output_frame, width=30)
        self.entry_output.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        tk.Button(output_frame, text="浏览", bg="#4CAF50", fg="white",
                  command=lambda: self.select_folder(self.entry_output)).pack(side=tk.LEFT)
        
        # 格式设置
        format_frame = tk.Frame(main_frame, bg="white")
        format_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(format_frame, text="目标格式:", bg="white").pack(side=tk.LEFT)
        self.entry_format = tk.Entry(format_frame, width=10)
        self.entry_format.pack(side=tk.LEFT, padx=5)
        self.entry_format.insert(0, "jpg")  # 默认格式
        
        # 提示文本
        tip_label = tk.Label(format_frame, text="(支持 jpg, png, jpeg, bmp)", 
                            fg="gray", bg="white", font=("Arial", 9))
        tip_label.pack(side=tk.LEFT, padx=10)
        
        # 操作按钮
        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="开始转换", bg="#2196F3", fg="white", 
                  width=15, command=self.on_convert_button_click).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="退出", bg="#f44336", fg="white", 
                  width=15, command=self.root.quit).pack(side=tk.LEFT, padx=10)
    
    def select_folder(self, entry_widget):
        folder = filedialog.askdirectory()
        if folder:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder)
    
    def convert_images(self, input_path, output_path, format):
        # 检查输入路径是否存在
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入文件夹不存在: {input_path}")
        
        # 创建输出文件夹
        os.makedirs(output_path, exist_ok=True)
        
        # 支持的图片格式
        supported_formats = ['jpg', 'jpeg', 'png', 'bmp']
        if format.lower() not in supported_formats:
            raise ValueError(f"不支持的格式: {format}. 支持格式: {', '.join(supported_formats)}")
        
        # 遍历文件夹中的所有图片
        for file in os.listdir(input_path):
            # 检查文件是否为图片
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                print(f"处理图片: {file}")
                # 构造图片的完整路径
                input_file = os.path.join(input_path, file)
                # 构造新文件名
                filename = os.path.splitext(file)[0]
                output_file = os.path.join(output_path, f"{filename}.{format}")
                
                try:
                    # 打开图片并转换格式
                    with Image.open(input_file) as img:
                        # 保存为指定格式
                        img.save(output_file, format=format.upper())
                except Exception as e:
                    messagebox.showerror(f"处理图片 {file} 时出错", str(e))
    
    def on_convert_button_click(self):
        # 获取输入值
        input_path = self.entry_input.get()
        output_path = self.entry_output.get()
        format = self.entry_format.get().strip().lower()
        
        # 验证输入
        if not input_path or not output_path or not format:
            messagebox.showerror("输入错误", "请填写所有字段")
            return
        
        if not os.path.isdir(input_path):
            messagebox.showerror("路径错误", "输入文件夹路径无效")
            return
        
        # 执行转换
        try:
            self.convert_images(input_path, output_path, format)
            messagebox.showinfo("成功", "图片格式转换完成！")
        except Exception as e:
            messagebox.showerror("转换错误", f"转换过程中出错: {str(e)}")


if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    # 创建应用程序实例
    app = ImageConverterApp(root)
    # 运行主循环
    root.mainloop()