import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime

class ImageBatchRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("图片批量命名工具")
        self.root.geometry("700x500")
        
        # 初始化变量
        self.folder_path = tk.StringVar()
        self.prefix_var = tk.StringVar(value="image")
        self.start_number_var = tk.StringVar(value="1")
        self.include_date_var = tk.BooleanVar()
        self.image_files = []
        
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
        
        # 文件夹选择部分
        ttk.Label(main_frame, text="选择文件夹:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        ttk.Button(main_frame, text="浏览", command=self.select_folder).grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # 命名规则设置
        rule_frame = ttk.LabelFrame(main_frame, text="命名规则", padding="10")
        rule_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        rule_frame.columnconfigure(1, weight=1)
        
        ttk.Label(rule_frame, text="前缀:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(rule_frame, textvariable=self.prefix_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=2, padx=(0, 20))
        
        ttk.Label(rule_frame, text="起始编号:").grid(row=0, column=2, sticky=tk.W, pady=2)
        ttk.Entry(rule_frame, textvariable=self.start_number_var, width=10).grid(row=0, column=3, sticky=tk.W, pady=2, padx=(0, 20))
        
        ttk.Checkbutton(rule_frame, text="包含日期", variable=self.include_date_var).grid(row=0, column=4, sticky=tk.W, pady=2)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="扫描图片", command=self.scan_images).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="预览名称", command=self.preview_names).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="执行重命名", command=self.rename_images).grid(row=0, column=2, padx=5)
        
        # 图片列表显示区域
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview来显示图片列表
        self.tree = ttk.Treeview(list_frame, columns=("old_name", "new_name"), show="headings")
        self.tree.heading("old_name", text="原文件名")
        self.tree.heading("new_name", text="新文件名")
        self.tree.column("old_name", width=250)
        self.tree.column("new_name", width=250)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def select_folder(self):
        """选择文件夹"""
        folder = filedialog.askdirectory(title="选择包含图片的文件夹")
        if folder:
            self.folder_path.set(folder)
            self.status_var.set(f"已选择文件夹: {folder}")
            
    def scan_images(self):
        """扫描文件夹中的图片文件"""
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("警告", "请先选择文件夹")
            return
            
        if not os.path.exists(folder):
            messagebox.showerror("错误", "选择的文件夹不存在")
            return
            
        # 支持的图片格式
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        
        # 清空现有列表
        self.image_files = []
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 扫描文件夹
        try:
            for filename in os.listdir(folder):
                _, ext = os.path.splitext(filename)
                if ext.lower() in image_extensions:
                    self.image_files.append(filename)
                    
            # 显示在列表中
            for filename in sorted(self.image_files):
                self.tree.insert("", tk.END, values=(filename, ""))
                
            self.status_var.set(f"找到 {len(self.image_files)} 个图片文件")
            messagebox.showinfo("完成", f"扫描完成，找到 {len(self.image_files)} 个图片文件")
            
        except Exception as e:
            messagebox.showerror("错误", f"扫描文件夹时出错: {str(e)}")
            
    def preview_names(self):
        """预览重命名结果"""
        if not self.image_files:
            messagebox.showwarning("警告", "请先扫描图片文件")
            return
            
        try:
            start_num = int(self.start_number_var.get())
        except ValueError:
            messagebox.showerror("错误", "起始编号必须是数字")
            return
            
        prefix = self.prefix_var.get()
        include_date = self.include_date_var.get()
        
        # 生成日期字符串
        date_str = ""
        if include_date:
            date_str = datetime.now().strftime("%Y%m%d") + "_"
            
        # 清空现有预览
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 生成新文件名并显示预览
        for i, filename in enumerate(sorted(self.image_files)):
            _, ext = os.path.splitext(filename)
            new_name = f"{prefix}_{date_str}{start_num + i:03d}{ext.lower()}"
            self.tree.insert("", tk.END, values=(filename, new_name))
            
        self.status_var.set("已生成命名预览")
        
    def rename_images(self):
        """执行重命名操作"""
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("警告", "请先选择文件夹")
            return
            
        # 检查是否有预览数据
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("警告", "请先预览命名结果")
            return
            
        # 确认操作
        result = messagebox.askyesno("确认", "确定要执行重命名操作吗？此操作不可撤销。")
        if not result:
            return
            
        success_count = 0
        try:
            for item in items:
                values = self.tree.item(item, "values")
                old_name, new_name = values
                
                old_path = os.path.join(folder, old_name)
                new_path = os.path.join(folder, new_name)
                
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    success_count += 1
                    
            self.status_var.set(f"重命名完成: {success_count} 个文件")
            messagebox.showinfo("完成", f"重命名完成，成功处理 {success_count} 个文件")
            
        except Exception as e:
            messagebox.showerror("错误", f"重命名过程中出错: {str(e)}")

def main():
    root = tk.Tk()
    app = ImageBatchRenamer(root)
    root.mainloop()

if __name__ == "__main__":
    main()