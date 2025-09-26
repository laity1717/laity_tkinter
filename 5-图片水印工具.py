# -*- coding: utf-8 -*-  python 3.12
# @Time    : 2025/9/10
# @Desc    : 图片水印工具
# @Author  : laity
# @Contact : 微信公众号：laity的渗透测试之路


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class ImageWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片水印工具")
        self.root.geometry("700x500")
        
        # 初始化变量
        self.image_path = tk.StringVar()
        self.watermark_text = tk.StringVar(value="水印文字")
        self.watermark_image_path = tk.StringVar()
        self.position_var = tk.StringVar(value="bottom-right")
        self.opacity_var = tk.StringVar(value="128")
        self.font_size_var = tk.StringVar(value="36")
        self.watermark_type_var = tk.StringVar(value="text")  # text 或 image
        self.original_image = None
        self.watermarked_image = None
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 图片选择部分
        ttk.Label(main_frame, text="选择图片:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.image_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        ttk.Button(main_frame, text="浏览", command=self.select_image).grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # 水印类型选择
        ttk.Label(main_frame, text="水印类型:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(main_frame, text="文字水印", variable=self.watermark_type_var, value="text", command=self.toggle_watermark_type).grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(main_frame, text="图片水印", variable=self.watermark_type_var, value="image", command=self.toggle_watermark_type).grid(row=1, column=1, sticky=tk.W, padx=100, pady=5)
        
        # 文字水印设置
        self.text_frame = ttk.Frame(main_frame)
        self.text_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(self.text_frame, text="水印文字:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(self.text_frame, textvariable=self.watermark_text, width=20).grid(row=0, column=1, sticky=tk.W, pady=2, padx=(0, 10))
        
        ttk.Label(self.text_frame, text="字体大小:").grid(row=0, column=2, sticky=tk.W, pady=2)
        ttk.Entry(self.text_frame, textvariable=self.font_size_var, width=10).grid(row=0, column=3, sticky=tk.W, pady=2, padx=(0, 10))
        
        # 图片水印设置
        self.image_frame = ttk.Frame(main_frame)
        self.image_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        self.image_frame.grid_remove()  # 默认隐藏
        
        ttk.Label(self.image_frame, text="水印图片:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(self.image_frame, textvariable=self.watermark_image_path, width=40).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(0, 5))
        ttk.Button(self.image_frame, text="浏览", command=self.select_watermark_image).grid(row=0, column=2, sticky=tk.W, pady=2)
        
        # 通用设置
        settings_frame = ttk.LabelFrame(main_frame, text="水印设置", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        settings_frame.columnconfigure(1, weight=1)
        
        ttk.Label(settings_frame, text="位置:").grid(row=0, column=0, sticky=tk.W, pady=2)
        position_combo = ttk.Combobox(settings_frame, textvariable=self.position_var, 
                                     values=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                                     state="readonly", width=15)
        position_combo.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(0, 20))
        
        ttk.Label(settings_frame, text="透明度:").grid(row=0, column=2, sticky=tk.W, pady=2)
        opacity_combo = ttk.Combobox(settings_frame, textvariable=self.opacity_var,
                                    values=["64", "128", "192", "255"],
                                    state="readonly", width=10)
        opacity_combo.grid(row=0, column=3, sticky=tk.W, pady=2)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="添加水印", command=self.add_watermark).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="预览", command=self.preview_watermark).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="保存图片", command=self.save_image).grid(row=0, column=2, padx=5)
        
        # 图片显示区域
        preview_frame = ttk.Frame(main_frame)
        preview_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        self.image_label = ttk.Label(preview_frame, text="图片预览区域")
        self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def toggle_watermark_type(self):
        """切换水印类型"""
        if self.watermark_type_var.get() == "text":
            self.text_frame.grid()
            self.image_frame.grid_remove()
        else:
            self.text_frame.grid_remove()
            self.image_frame.grid()
            
    def select_image(self):
        """选择主图片"""
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.image_path.set(file_path)
            self.status_var.set(f"已选择图片: {os.path.basename(file_path)}")
            
    def select_watermark_image(self):
        """选择水印图片"""
        file_path = filedialog.askopenfilename(
            title="选择水印图片",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.watermark_image_path.set(file_path)
            self.status_var.set(f"已选择水印图片: {os.path.basename(file_path)}")
            
    def load_image(self, image_path):
        """加载图片"""
        try:
            return Image.open(image_path).convert("RGBA")
        except Exception as e:
            raise Exception(f"加载图片失败: {str(e)}")
            
    def add_text_watermark(self, base_image):
        """添加文字水印"""
        # 创建水印图层
        txt_layer = Image.new('RGBA', base_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        
        # 设置字体
        try:
            font_size = int(self.font_size_var.get())
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # 如果无法加载指定字体，使用默认字体
            font_size = int(self.font_size_var.get())
            font = ImageFont.load_default()
        
        # 获取文字尺寸
        text = self.watermark_text.get()
        try:
            # Pillow 8.0.0+ 版本
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            # 旧版本
            text_width, text_height = draw.textsize(text, font=font)
        
        # 计算水印位置
        position = self.position_var.get()
        x, y = self.calculate_position(base_image.size, (text_width, text_height), position)
        
        # 设置透明度
        opacity = int(self.opacity_var.get())
        rgba = (255, 255, 255, opacity)  # 白色文字，可调节透明度
        
        # 绘制文字水印
        draw.text((x, y), text, font=font, fill=rgba)
        
        # 合并图层
        watermarked = Image.alpha_composite(base_image, txt_layer)
        return watermarked.convert("RGB")  # 转换为RGB格式以支持更多格式保存
        
    def add_image_watermark(self, base_image):
        """添加图片水印"""
        try:
            # 加载水印图片
            watermark = self.load_image(self.watermark_image_path.get())
            
            # 设置透明度
            opacity = int(self.opacity_var.get())
            if opacity < 255:
                # 调整水印透明度
                alpha = watermark.split()[-1]  # 获取alpha通道
                alpha = alpha.point(lambda p: min(p, opacity))
                watermark.putalpha(alpha)
            
            # 计算水印位置
            base_width, base_height = base_image.size
            watermark_width, watermark_height = watermark.size
            
            # 如果水印太大，按比例缩小
            max_size = min(base_width, base_height) // 4
            if max(watermark_width, watermark_height) > max_size:
                ratio = max_size / max(watermark_width, watermark_height)
                new_width = int(watermark_width * ratio)
                new_height = int(watermark_height * ratio)
                watermark = watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)
                watermark_width, watermark_height = watermark.size
            
            x, y = self.calculate_position(base_image.size, (watermark_width, watermark_height), self.position_var.get())
            
            # 创建新图层并粘贴水印
            if base_image.mode != "RGBA":
                base_image = base_image.convert("RGBA")
                
            watermarked = base_image.copy()
            watermarked.paste(watermark, (x, y), watermark)
            
            return watermarked.convert("RGB")  # 转换为RGB格式
            
        except Exception as e:
            raise Exception(f"添加图片水印失败: {str(e)}")
            
    def calculate_position(self, base_size, watermark_size, position):
        """计算水印位置"""
        base_width, base_height = base_size
        watermark_width, watermark_height = watermark_size
        margin = 20  # 边距
        
        if position == "top-left":
            x, y = margin, margin
        elif position == "top-right":
            x, y = base_width - watermark_width - margin, margin
        elif position == "bottom-left":
            x, y = margin, base_height - watermark_height - margin
        elif position == "bottom-right":
            x, y = base_width - watermark_width - margin, base_height - watermark_height - margin
        else:  # center
            x, y = (base_width - watermark_width) // 2, (base_height - watermark_height) // 2
            
        return x, y
        
    def add_watermark(self):
        """添加水印"""
        if not self.image_path.get():
            messagebox.showerror("错误", "请先选择图片")
            return
            
        try:
            # 加载原始图片
            self.original_image = self.load_image(self.image_path.get())
            self.status_var.set("正在添加水印...")
            
            # 根据类型添加水印
            if self.watermark_type_var.get() == "text":
                self.watermarked_image = self.add_text_watermark(self.original_image)
            else:
                if not self.watermark_image_path.get():
                    messagebox.showerror("错误", "请选择水印图片")
                    return
                self.watermarked_image = self.add_image_watermark(self.original_image)
                
            self.status_var.set("水印添加完成")
            messagebox.showinfo("成功", "水印已添加")
            
        except Exception as e:
            self.status_var.set("操作失败")
            messagebox.showerror("错误", f"添加水印失败: {str(e)}")
            
    def preview_watermark(self):
        """预览水印效果"""
        if not self.image_path.get():
            messagebox.showerror("错误", "请先选择图片")
            return
            
        try:
            # 如果还没有处理过图片，则先添加水印
            if not self.watermarked_image:
                self.add_watermark()
                
            if self.watermarked_image:
                self.display_image(self.watermarked_image)
                self.status_var.set("显示预览")
                
        except Exception as e:
            messagebox.showerror("错误", f"预览失败: {str(e)}")
            
    def display_image(self, image):
        """显示图片"""
        try:
            # 调整图片大小以适应显示区域
            max_width, max_height = 400, 300
            img_width, img_height = image.size
            
            # 计算缩放比例
            ratio = min(max_width/img_width, max_height/img_height, 1.0)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            # 缩放图片用于显示
            display_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.display_photo = ImageTk.PhotoImage(display_img)
            
            # 更新标签显示
            self.image_label.configure(image=self.display_photo, text="")
            
        except Exception as e:
            print(f"显示图片失败: {str(e)}")
            
    def save_image(self):
        """保存图片"""
        if not self.watermarked_image:
            messagebox.showerror("错误", "没有可保存的图片，请先添加水印")
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
                self.watermarked_image.save(file_path)
                self.status_var.set(f"图片已保存到: {file_path}")
                messagebox.showinfo("成功", f"图片已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存图片失败: {str(e)}")

def main():
    root = tk.Tk()
    app = ImageWatermarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()