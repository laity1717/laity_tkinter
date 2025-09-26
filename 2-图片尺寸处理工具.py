# -*- coding: utf-8 -*-  python 3.12
# @Time    : 2025/9/10
# @Desc    : 图片尺寸处理工具
# @Author  : laity
# @Contact : 微信公众号：laity的渗透测试之路


import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageResizerApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("图片尺寸调整工具")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # 初始化变量
        self.current_image = None
        self.current_image_path = None
        self.processed_image = None
        
        # 创建菜单
        self.create_menu()
        
        # 初始化UI组件
        self.setup_ui()
        
        # 默认显示批量处理界面
        self.show_batch_mode()
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 处理菜单
        process_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="处理", menu=process_menu)
        process_menu.add_command(label="单张图片处理", command=self.show_single_mode)
        process_menu.add_command(label="批量图片处理", command=self.show_batch_mode)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def setup_ui(self):
        """设置UI组件"""
        # 创建主框架
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建单张图片处理界面
        self.create_single_mode_ui()
        
        # 创建批量处理界面
        self.create_batch_mode_ui()
        
        # 创建预览区域
        self.create_preview_area()
    
    def create_single_mode_ui(self):
        """创建单张图片处理界面"""
        self.single_frame = tk.Frame(self.main_frame)
        
        # 图片文件选择
        file_frame = tk.Frame(self.single_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(file_frame, text="图片文件:").pack(side=tk.LEFT)
        self.entry_single_file = tk.Entry(file_frame, width=50)
        self.entry_single_file.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        tk.Button(file_frame, text="浏览", 
                  command=self.select_single_file).pack(side=tk.LEFT)
        
        # 尺寸设置
        size_frame = tk.Frame(self.single_frame)
        size_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(size_frame, text="新宽度:").pack(side=tk.LEFT)
        self.entry_single_width = tk.Entry(size_frame, width=10)
        self.entry_single_width.pack(side=tk.LEFT, padx=5)
        
        tk.Label(size_frame, text="新高度:").pack(side=tk.LEFT, padx=(20, 0))
        self.entry_single_height = tk.Entry(size_frame, width=10)
        self.entry_single_height.pack(side=tk.LEFT, padx=5)
        
        # 保持宽高比选项
        self.maintain_ratio_var = tk.BooleanVar()
        tk.Checkbutton(size_frame, text="保持宽高比", variable=self.maintain_ratio_var).pack(side=tk.LEFT, padx=(20, 0))
        
        # 操作按钮
        button_frame = tk.Frame(self.single_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="加载图片", 
                  command=self.load_single_image, width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="调整尺寸", 
                  command=self.resize_single_image, width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="保存图片", 
                  command=self.save_single_image, width=12).pack(side=tk.LEFT, padx=5)
    
    def create_batch_mode_ui(self):
        """创建批量处理界面"""
        self.batch_frame = tk.Frame(self.main_frame)
        
        # 源文件夹选择
        source_frame = tk.Frame(self.batch_frame)
        source_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(source_frame, text="原图片文件夹:").pack(side=tk.LEFT)
        self.entry_old_path = tk.Entry(source_frame, width=50)
        self.entry_old_path.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        tk.Button(source_frame, text="浏览", 
                  command=lambda: self.select_folder(self.entry_old_path)).pack(side=tk.LEFT)
        
        # 目标文件夹选择
        dest_frame = tk.Frame(self.batch_frame)
        dest_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(dest_frame, text="新图片文件夹:").pack(side=tk.LEFT)
        self.entry_new_path = tk.Entry(dest_frame, width=50)
        self.entry_new_path.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        tk.Button(dest_frame, text="浏览", 
                  command=lambda: self.select_folder(self.entry_new_path)).pack(side=tk.LEFT)
        
        # 尺寸设置
        size_frame = tk.Frame(self.batch_frame)
        size_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(size_frame, text="新宽度:").pack(side=tk.LEFT)
        self.entry_width = tk.Entry(size_frame, width=10)
        self.entry_width.pack(side=tk.LEFT, padx=5)
        
        tk.Label(size_frame, text="新高度:").pack(side=tk.LEFT, padx=(20, 0))
        self.entry_height = tk.Entry(size_frame, width=10)
        self.entry_height.pack(side=tk.LEFT, padx=5)
        
        # 操作按钮
        button_frame = tk.Frame(self.batch_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="调整图片尺寸", 
                  command=self.on_resize_button_click, width=15).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="退出", 
                  command=self.root.quit, width=15).pack(side=tk.LEFT, padx=10)
    
    def create_preview_area(self):
        """创建预览区域"""
        preview_frame = tk.Frame(self.main_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(preview_frame, text="预览区域:").pack(anchor=tk.W)
        
        self.preview_label = tk.Label(preview_frame, text="暂无预览", bg="lightgray", width=60, height=10)
        self.preview_label.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def show_single_mode(self):
        """显示单张图片处理界面"""
        self.batch_frame.pack_forget()
        self.single_frame.pack(fill=tk.X)
    
    def show_batch_mode(self):
        """显示批量处理界面"""
        self.single_frame.pack_forget()
        self.batch_frame.pack(fill=tk.X)
    
    def show_about(self):
        """显示关于信息"""
        messagebox.showinfo("关于", "图片尺寸调整工具\n支持单张和批量图片处理")
    
    def select_single_file(self):
        """选择单个图片文件"""
        file_path = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.entry_single_file.delete(0, tk.END)
            self.entry_single_file.insert(0, file_path)
    
    def select_folder(self, entry_widget):
        """选择文件夹"""
        folder = filedialog.askdirectory()
        if folder:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder)
    
    def load_single_image(self):
        """加载单张图片"""
        file_path = self.entry_single_file.get()
        if not file_path:
            messagebox.showerror("错误", "请选择图片文件")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("错误", "文件不存在")
            return
        
        try:
            self.current_image = Image.open(file_path)
            self.current_image_path = file_path
            
            # 显示原始尺寸
            width, height = self.current_image.size
            self.entry_single_width.delete(0, tk.END)
            self.entry_single_width.insert(0, str(width))
            self.entry_single_height.delete(0, tk.END)
            self.entry_single_height.insert(0, str(height))
            
            # 显示预览
            self.display_image_preview(self.current_image)
            
            messagebox.showinfo("成功", "图片加载成功")
        except Exception as e:
            messagebox.showerror("错误", f"加载图片失败: {str(e)}")
    
    def resize_single_image(self):
        """调整单张图片尺寸"""
        if not self.current_image:
            messagebox.showerror("错误", "请先加载图片")
            return
        
        try:
            new_width = int(self.entry_single_width.get())
            new_height = int(self.entry_single_height.get())
        except ValueError:
            messagebox.showerror("错误", "宽度和高度必须是整数")
            return
        
        try:
            if self.maintain_ratio_var.get():
                # 保持宽高比
                original_width, original_height = self.current_image.size
                ratio = min(new_width/original_width, new_height/original_height)
                adjusted_width = int(original_width * ratio)
                adjusted_height = int(original_height * ratio)
                self.processed_image = self.current_image.resize((adjusted_width, adjusted_height), Image.Resampling.LANCZOS)
            else:
                # 直接调整到指定尺寸
                self.processed_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 显示预览
            self.display_image_preview(self.processed_image)
            messagebox.showinfo("成功", "图片尺寸调整完成")
        except Exception as e:
            messagebox.showerror("错误", f"调整图片尺寸失败: {str(e)}")
    
    def save_single_image(self):
        """保存单张图片"""
        if not self.processed_image and not self.current_image:
            messagebox.showerror("错误", "没有可保存的图片")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存图片",
            defaultextension=".png",
            filetypes=[
                ("PNG 文件", "*.png"),
                ("JPEG 文件", "*.jpg *.jpeg"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                image_to_save = self.processed_image if self.processed_image else self.current_image
                image_to_save.save(file_path)
                messagebox.showinfo("成功", f"图片已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存图片失败: {str(e)}")
    
    def display_image_preview(self, image):
        """显示图片预览"""
        try:
            # 调整图片大小以适应预览区域
            max_width, max_height = 400, 200
            img_width, img_height = image.size
            
            # 计算缩放比例
            ratio = min(max_width/img_width, max_height/img_height, 1.0)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            # 缩放图片用于显示
            preview_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.preview_photo = ImageTk.PhotoImage(preview_img)
            
            # 更新预览标签
            self.preview_label.configure(image=self.preview_photo, text="", bg="white")
        except Exception as e:
            print(f"显示预览失败: {str(e)}")
    
    def resize_images(self, old_images_path, new_images_path, new_width, new_height):
        """批量调整图片尺寸"""
        # 如果没有指定的文件夹，则创建文件夹
        if not os.path.exists(new_images_path):
            os.makedirs(new_images_path)
        
        success_count = 0
        total_count = 0
        
        # 遍历文件夹中的所有图片
        for file in os.listdir(old_images_path):
            total_count += 1
            print(f"处理图片: {file}")
            # 构造图片的完整路径
            old_file_path = os.path.join(old_images_path, file)
            # 构造新图片的完整路径
            new_file_path = os.path.join(new_images_path, file)
            
            try:
                # 打开图片
                with Image.open(old_file_path) as img:
                    # 调整图片尺寸
                    img_resized = img.resize((new_width, new_height))
                    img_resized.save(new_file_path)
                    success_count += 1
            except Exception as e:
                print(f"处理图片 {file} 时出错: {str(e)}")
        
        return success_count, total_count
    
    def on_resize_button_click(self):
        """批量处理按钮点击事件"""
        # 获取输入框中的值
        old_images_path = self.entry_old_path.get()
        new_images_path = self.entry_new_path.get()
        
        # 验证尺寸输入
        try:
            new_width = int(self.entry_width.get())
            new_height = int(self.entry_height.get())
        except ValueError:
            messagebox.showerror("输入错误", "宽度和高度必须是整数")
            return
        
        # 验证路径输入
        if not old_images_path or not new_images_path:
            messagebox.showerror("输入错误", "请选择源文件夹和目标文件夹")
            return
        
        if not os.path.isdir(old_images_path):
            messagebox.showerror("路径错误", "源文件夹路径无效")
            return
        
        # 调用图片调整函数
        try:
            success_count, total_count = self.resize_images(old_images_path, new_images_path, new_width, new_height)
            messagebox.showinfo("完成", f"图片尺寸调整完成！\n成功处理: {success_count}/{total_count} 张图片")
        except Exception as e:
            messagebox.showerror("处理错误", f"处理过程中出错: {str(e)}")


if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    # 创建应用程序实例
    app = ImageResizerApp(root)
    # 运行主循环
    root.mainloop()