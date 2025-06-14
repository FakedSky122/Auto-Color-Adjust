from PIL import Image, ImageStat, ImageEnhance, ImageTk
import numpy as np
import tkinter as tk
from tkinter import CENTER, E, N, W, filedialog, HORIZONTAL
# 打开图片
img = None
print('（调试信息将在控制台显示）')
##### GUI
root = tk.Tk()
root.geometry("960x540") #设置分辨率
menubar = tk.Menu(root)
root.title('tk _深度图像调色')

#enhanced_image3 = None  # 预定义全局变量
def open_img():
    input_image_path = filedialog.askopenfilename()
    global img, img_size, width, height, img_show, viewtips, label_img, v, run, style, offset, enhanced_image3, mixw
    img = Image.open(input_image_path)
    img_size = img.size
    width = img.width
    height = img.height
    img_show = img.resize((int(width/height*144), 144)) #拉伸图片以用来预览
    img_show = ImageTk.PhotoImage(img_show)
    viewtips = tk.Label(root, text='预览图片：')
    viewtips.pack()
    label_img = tk.Label(root, image=img_show)
    label_img.pack()
        # 标签
    tk.Label(root, text="选择图片的风格:").pack(side='top')

        # 变量
    v = tk.IntVar()

        # 单选按钮
    tk.Radiobutton(root, text="暗调", padx=20, variable=v, value=0).pack(anchor=W)
    tk.Radiobutton(root, text="中性", padx=20, variable=v, value=1).pack(anchor=W)
    tk.Radiobutton(root, text="亮调", padx=20, variable=v, value=2).pack(anchor=W)
    def apply_style():
        global offset
        print('风格应用成功')
        style = v.get() #转换至数字
        offset = 0.67 + (style/3)
        print('style_choice=',style,', offset=',offset)
    global var1,var2,var3,var4
    var01 = tk.IntVar()
    var02 = tk.IntVar()
    var03 = tk.IntVar()
    var04 = tk.IntVar()
    check1 = tk.Checkbutton(root,text='调整亮度',variable=var01) #创建一个复选框
    check1.pack()
    check2 = tk.Checkbutton(root,text='调整对比度',variable=var02) #创建一个复选框
    check2.pack()
    check3 = tk.Checkbutton(root,text='调整饱和度',variable=var03) #创建一个复选框
    check3.pack()
    check4 = tk.Checkbutton(root,text='校正色温',variable=var04) #创建一个复选框
    check4.pack()

    #创建强度滑块
    mixw0 = tk.DoubleVar()
    mixscale = tk.Scale(root,variable=mixw0,orient=HORIZONTAL,label='混合强度：',length=200)
    mixscale.pack()
    def apply_check():
        global var1,var2,var3,var4,mixw
        var1 = var01.get()
        var2 = var02.get()
        var3 = var03.get()
        var4 = var04.get()
        mixw = mixw0.get()
        print('可选项应用成功')
    apply_button1 = tk.Button(root, text="应用样式", command=apply_style)
    apply_button1.pack()
    apply_button2 = tk.Button(root, text="应用选择", command=apply_check)
    apply_button2.pack()
    def run():

        global enhanced_image4
        # 转换为不同通道的图
        gray_img = img.convert('L')
        hsv_img = img.convert('HSV')
        blue_img = Image.open('blue.jpg')
        orange_img = Image.open('orange.jpg')
        blue_img = blue_img.resize(img_size)
        orange_img = orange_img.resize(img_size)
        # 获取S通道数据
        saturation_data = np.array(hsv_img)[:,:,1]
        # 获取像素数据
        pixels = np.array(img)
        # 计算RGB通道的平均值
        r_mean = np.mean(pixels[:,:,0])
        g_mean = np.mean(pixels[:,:,1])
        b_mean = np.mean(pixels[:,:,2])

        #计算数值
        mean_brightness = np.mean(np.array(gray_img)) #亮度
        mean_contrast = ImageStat.Stat(gray_img).stddev[0] #对比度
        mean_saturation = np.mean(saturation_data)    #饱和度
        color_temp = r_mean / b_mean
        print('brightness:',mean_brightness)
        print('contrast:',mean_contrast)
        print('saturation:',mean_saturation)
        print('color_temp',color_temp)
        print('mixw=',mixw)
        ###
        #设置标准数值
        std_brightness = 105 * offset
        std_contrast = 64
        std_saturation = 110 * (1/offset)
        ### 计算调整值
        if mean_brightness == 0:
            mean_brightness = 1
        if mean_contrast == 0:
            mean_contrast = 1
        if mean_saturation == 0:
            mean_saturation = 1

        new_brightness = std_brightness/mean_brightness
        new_contrast = std_contrast/mean_contrast
        new_saturation = std_saturation/mean_saturation
        print('new_brightness:',new_brightness)
        print('new_contrast:',new_contrast)
        print('new_saturation:',new_saturation)
        print()
        ### 设置增强器 并增强
        if var1 == 1:
            enhancer0 = ImageEnhance.Brightness(img)
            enhanced_image0 = enhancer0.enhance(new_brightness) #亮度调整
        else:
            enhanced_image0 = img
        if var2 == 1:
            enhancer1 = ImageEnhance.Contrast(enhanced_image0)
            enhanced_image1 = enhancer1.enhance(new_contrast)   #对比度调整
        else:
            enhanced_image1 = enhanced_image0
        if var3 == 1:
            enhancer2 = ImageEnhance.Color(enhanced_image1)
            enhanced_image2 = enhancer2.enhance(new_saturation) #饱和度调整
        else:
            enhanced_image2 = enhanced_image1
        if var4 == 1:
            if color_temp > 1:                                  #色温调整
                alpha = (color_temp - 1) / 1.5
                enhanced_image3 = Image.blend(enhanced_image2,blue_img,alpha)
            else:
                alpha = (color_temp - 1) / 1.5
                enhanced_image3 = Image.blend(enhanced_image2,orange_img,alpha)
        else:
            enhanced_image3 = enhanced_image2
        enhanced_image4 = Image.blend(img,enhanced_image3,mixw/100)
        #else:
            #print("图片亮度正常")
            #enhanced_image = img
        enhanced_image4.show()
        output_image_path = filedialog.asksaveasfilename()
        if '.jpg' in output_image_path or '.png' in output_image_path:
            enhanced_image4.save(output_image_path)
        else:
            enhanced_image4.save(output_image_path+'.jpg')

    run = tk.Button(root, text='开始运行并保存',command=run)
    run.pack()
    #return enhanced_image3

    #在顶层窗口menubar中加入下拉窗口filemenu
filemenu = tk.Menu(menubar, tearoff=False)
filemenu.add_command(label="打开文件",command=open_img)
#filemenu.add_command(label="保存",command=save_img)
filemenu.add_separator()
filemenu.add_command(label="退出",command=root.quit)
menubar.add_cascade(label="文件", menu=filemenu) #为filemenu命名为'文件'
root.config(menu=menubar)

root.mainloop()
#####