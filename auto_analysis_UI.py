import sys, os

from PyQt5 import uic
from PyQt5.QtCore import  QProcess,QSettings,Qt,pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QColorDialog, QFileDialog,QMessageBox,QSplashScreen
from PyQt5.QtGui import QPalette, QColor, QIcon, QPixmap



class appwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.ui = uic.loadUi('./data_filter.ui')

        #----------logo及标题-----------
        self.ui.setWindowIcon(QIcon('./logo2.ico'))
        self.ui.setWindowTitle('【佳学基因】数据筛选工具(beta_v0.5)')

        #----------按钮控件-----------
        btn   = self.ui.pushButton      # 第二次_选择文件按钮
        btn_2 = self.ui.pushButton_2    # 第二次_高频突变_颜色按钮
        btn_3 = self.ui.pushButton_3    # 第二次_致病性_颜色按钮
        btn_4 = self.ui.pushButton_4    # 第二次_纯合_颜色按钮
        btn_5 = self.ui.pushButton_5    # 第二次_同义突变_颜色按钮
        btn_6 = self.ui.pushButton_6    # 第二次_突变类型_颜色按钮
        btn_7 = self.ui.pushButton_7    # 第二次_导出文件_按钮

        btn_8  = self.ui.pushButton_8    # 原始_选择文件按钮
        btn_9  = self.ui.pushButton_9    # 原始_导出OMIM关键词_按钮
        btn_10 = self.ui.pushButton_10   # 原始_导出HGMD关键词_按钮
        btn_11 = self.ui.pushButton_11   # 原始_导出文件按钮

        btn_12 = self.ui.pushButton_12   # 第一次_选择文件按钮
        btn_13 = self.ui.pushButton_13   # 第一次_人群比_颜色按钮
        btn_14 = self.ui.pushButton_14   # 第一次_突变类型_颜色按钮
        btn_15 = self.ui.pushButton_15   # 第一次_相关基因_颜色按钮
        btn_16 = self.ui.pushButton_16   # 第一次_导出文件按钮
        
        #导入文件
        btn.clicked.connect(self.getFileName_second)
        btn.setCursor(Qt.PointingHandCursor)    #导入第二次筛选表
        btn_8.clicked.connect(self.getFileName_raw)
        btn_8.setCursor(Qt.PointingHandCursor)     #导入原始数据表
        btn_12.clicked.connect(self.getFileName_first)
        btn_12.setCursor(Qt.PointingHandCursor)  #导入第一次筛选表

        #导出文件
        btn_7.clicked.connect(self.output_second)
        btn_7.setCursor(Qt.PointingHandCursor)
        btn_11.clicked.connect(self.output_raw)
        btn_11.setCursor(Qt.PointingHandCursor)
        btn_16.clicked.connect(self.output_first)
        btn_16.setCursor(Qt.PointingHandCursor)

        #第二次表中的颜色
        btn_2.clicked.connect(self.getColor_eas)
        btn_2.setCursor(Qt.PointingHandCursor)    # 第二次_高频突变_颜色按钮
        btn_3.clicked.connect(self.getColor_pathogenic)
        btn_3.setCursor(Qt.PointingHandCursor)    # 第二次_致病性_颜色按钮
        btn_4.clicked.connect(self.getColor_GT) 
        btn_4.setCursor(Qt.PointingHandCursor)   # 第二次_纯合_颜色按钮
        btn_5.clicked.connect(self.getColor_synonymous) 
        btn_5.setCursor(Qt.PointingHandCursor)   # 第二次_同义突变_颜色按钮
        btn_6.clicked.connect(self.getColor_func)
        btn_6.setCursor(Qt.PointingHandCursor)    # 第二次_突变类型_颜色按钮

        #第一次表中的颜色
        btn_13.clicked.connect(self.getColor_eas_F) 
        btn_13.setCursor(Qt.PointingHandCursor)   # 第二次_高频突变_颜色按钮
        btn_14.clicked.connect(self.getColor_func_F)
        btn_14.setCursor(Qt.PointingHandCursor)
        btn_15.clicked.connect(self.getColor_OMIM) 
        btn_15.setCursor(Qt.PointingHandCursor)
        
        #设置颜色模块的保存和调用功能
        self.settings = QSettings("config", 'QSettings')
        self.settings.setIniCodec('UTF-8')
        #在第二次筛选表中，应用上次设置的颜色
        color_eas = self.settings.value('labelColor_eas', "")
        color_eas_name = self.settings.value('labelColorName_eas','')
        try:
            self.ui.label_5.setStyleSheet(f"background-color: {color_eas.name()};")
        except:
            pass
        self.ui.label_5.setText(color_eas_name)

        color_pathogenic = self.settings.value('labelColor_pathogenic', "")
        color_pathogenic_name = self.settings.value('labelColorName_pathogenic','')
        try:
            self.ui.label_7.setStyleSheet(f"background-color: {color_pathogenic.name()};")
        except:
            pass
        self.ui.label_7.setText(color_pathogenic_name)

        color_GT = self.settings.value('labelColor_GT', "")
        color_GT_name = self.settings.value('labelColorName_GT','')
        try:
            self.ui.label_9.setStyleSheet(f"background-color: {color_GT.name()};")
        except:
            pass
        self.ui.label_9.setText(color_GT_name)

        color_synonymous = self.settings.value('labelColor_synonymous', "")
        color_synonymous_name = self.settings.value('labelColorName_synonymous','')
        
        try:
            self.ui.label_11.setStyleSheet(f"background-color: {color_synonymous.name()};")
        except:
            pass
        self.ui.label_11.setText(color_synonymous_name)

        color_func = self.settings.value('labelColor_func', "")
        color_func_name = self.settings.value('labelColorName_func','')
        try:
            self.ui.label_13.setStyleSheet(f"background-color: {color_func.name()};")
        except:
            pass
        self.ui.label_13.setText(color_func_name)

        #在第一次筛选表中，应用上次设置的颜色
        color_eas_F = self.settings.value('labelColor_eas_F', "")
        color_eas_name_F = self.settings.value('labelColorName_eas_F','')
        try:
            self.ui.label_17.setStyleSheet(f"background-color: {color_eas_F.name()};")
        except:
            pass
        self.ui.label_17.setText(color_eas_name_F)

        color_func_F = self.settings.value('labelColor_func_F', "")
        color_func_name_F = self.settings.value('labelColorName_func_F','')
        try:
            self.ui.label_19.setStyleSheet(f"background-color: {color_func_F.name()};")
        except:
            pass
        self.ui.label_19.setText(color_func_name_F)

        color_OMIM = self.settings.value('labelColor_OMIM', "")
        color_OMIM_name = self.settings.value('labelColorName_OMIM','')
        try:
            self.ui.label_21.setStyleSheet(f"background-color: {color_OMIM.name()};")
        except:
            pass
        self.ui.label_21.setText(color_OMIM_name)
        

        

        #----------其他控件-----------
        self.process_second = None
        self.process_raw = None
        self.process_first = None


    #——————————————文件导入——————————————————
    #获取文件路径(第二次筛选表)
    def getFileName_second(self):
        fileName_second, filetype = QFileDialog.getOpenFileName(self,
        '选取文件', './', 'Excel Files (*.xlsx);;All Files(*)')
        self.ui.label_3.setText(fileName_second)
        #return fileName_second
    #获取文件路径(原始数据表)
    def getFileName_raw(self):
        fileName_raw, filetype = QFileDialog.getOpenFileName(self,
        '选取文件', './', 'Excel Files (*.xlsx);;All Files(*)')
        self.ui.label_14.setText(fileName_raw)
        #return fileName_raw
    #获取文件路径(第一次筛选表)
    def getFileName_first(self):
        fileName_first, filetype = QFileDialog.getOpenFileName(self,
        '选取文件', './', 'Excel Files (*.xlsx);;All Files(*)')
        self.ui.label_15.setText(fileName_first)
        #return fileName_first

    #——————————————文件导出——————————————————
    #———————第二次筛选表——————————
    def output_second(self):
        filename_second = self.ui.label_3.text()
        color_second_eas = self.ui.label_5.text()
        color_second_pathogenic = self.ui.label_7.text()
        color_second_GT = self.ui.label_9.text()
        color_second_synonymous = self.ui.label_11.text()
        color_second_func = self.ui.label_13.text()
        self.process_second = QProcess()
        if self.process_second is not None:
            self.process_second.readyReadStandardOutput.connect(self.handle_stderr)
            args_second = []
            # process_path_second = r'./auto_analysis_second.exe'
            # args_second.append(process_path_second)#sys.argv[0]为py文件名，此处用于获取路径
            args_second.append(filename_second)#sys.argv[1]
            args_second.append(color_second_eas)#sys.argv[2]
            args_second.append(color_second_pathogenic)#sys.argv[3]
            args_second.append(color_second_GT)#sys.argv[4]
            args_second.append(color_second_synonymous)#sys.argv[5]
            args_second.append(color_second_func)#sys.argv[6]
            self.process_second.start('./auto_analysis_second.exe', args_second)
            
            self.ui.label_22.setText('正在导出第二次筛选表，请稍后…………')
            self.process_second.finished.connect(self.process_second_finished)

    def process_second_finished(self):
        if os.path.exists(f'【Marked】{self.ui.label_3.text().split("/")[-1]}'):
            self.ui.label_22.setText('已导出第二次筛选表，请核对！')
            QMessageBox.information(self, '提示', '已导出第二次筛选表，请核对！')
        else:
            self.ui.label_22.setText('导出失败，请重试！')
    
    #———————原始数据表——————————    
    def output_raw(self):
        filename_raw = self.ui.label_14.text()
        keywords_OMIM = self.ui.lineEdit.text()
        keywords_HGMD = self.ui.lineEdit_2.text()
        self.process_raw = QProcess()
        if self.process_raw is not None:
            self.process_raw.readyReadStandardOutput.connect(self.handle_stderr)
            args_raw = []
            # process_path_raw = r'./auto_analysis_raw.exe'
            # args_raw.append(process_path_raw)#sys.argv[0]为py文件名，此处用于获取路径
            args_raw.append(filename_raw)#sys.argv[1]
            args_raw.append(keywords_OMIM)#sys.argv[2]
            args_raw.append(keywords_HGMD)#sys.argv[3]
            self.process_raw.start('./auto_analysis_raw.exe', args_raw)
            self.ui.label_23.setText('正在导出原始数据表，请稍后…………')
            self.process_raw.finished.connect(self.process_raw_finished)

    def process_raw_finished(self):
        if os.path.exists(f'【Keywords_HGMD】{self.ui.label_14.text().split("/")[-1]}'):
            self.ui.label_23.setText('已导出原始数据表，请核对！')
            QMessageBox.information(self, '提示', '已导出原始数据表，请核对！')
        else:
            self.ui.label_23.setText('导出失败，请重试！')

    #———————第一次筛选表——————————
    def output_first(self):
        filename_first = self.ui.label_15.text()
        color_first_eas = self.ui.label_17.text()
        color_first_func = self.ui.label_19.text()
        color_first_OMIM = self.ui.label_21.text()
        self.process_first = QProcess()
        if self.process_first is not None:
            self.process_first.readyReadStandardOutput.connect(self.handle_stderr)
            args_first = []
            # process_path_first = r'./auto_analysis_first.exe'
            # args_first.append(process_path_first)#sys.argv[0]为py文件名，此处用于获取路径
            args_first.append(filename_first)#sys.argv[1]
            args_first.append(color_first_eas)#sys.argv[2]
            args_first.append(color_first_func)#sys.argv[3]
            args_first.append(color_first_OMIM)#sys.argv[4]
            self.process_first.start('./auto_analysis_first.exe', args_first)
            self.ui.label_24.setText('正在导出第一次筛选表，请稍后…………')
            self.process_first.finished.connect(self.process_first_finished)

    def process_first_finished(self):
        if os.path.exists(f'【Marked】{self.ui.label_15.text().split("/")[-1]}'):
            self.ui.label_24.setText('已导出第一次筛选表，请核对！')
            QMessageBox.information(self, '提示', '已导出第一次筛选表，请核对！')
        else:
            self.ui.label_24.setText('导出失败，请重试！')
    
    #——————————————异常处理——————————————————
    def handle_stderr(self):
        if self.process is not None:
            data = self.process.readAllStandardError()
            stderr = bytes(data).decode("utf8")
            print(stderr)

    #——————————————第二次筛选表颜色设置——————————————————
    def getColor_eas(self):
        default_color_eas = QColor('#c2c2c2') #默认灰色
        color_eas = QColorDialog.getColor(default_color_eas)
        p_eas = QPalette()
        p_eas.setColor(QPalette.Window, color_eas)#Window是窗口，用于背景色设置，WindowText是文本，用于字体色设置
        self.ui.label_5.setAutoFillBackground(True)#是否填充背景，改文本颜色时要注掉或填False
        self.ui.label_5.setPalette(p_eas)
        self.ui.label_5.setText(color_eas.name())#颜色名称，用于传递给其他函数
        self.settings.setValue('labelColor_eas', color_eas)#保存颜色设置
        self.settings.setValue('labelColorName_eas', color_eas.name())
        
    def getColor_pathogenic(self):
        default_color_pathogenic = QColor('#00ff00') #默认绿色
        color_pathogenic = QColorDialog.getColor(default_color_pathogenic)
        p_pathogenic = QPalette()
        p_pathogenic.setColor(QPalette.Window, color_pathogenic)#Window是窗口，用于背景色设置，WindowText是文本，用于字体色设置
        self.ui.label_7.setAutoFillBackground(True)#是否填充背景，改文本颜色时要注掉或填False
        self.ui.label_7.setPalette(p_pathogenic)
        self.ui.label_7.setText(color_pathogenic.name())#颜色名称，用于传递给其他函数
        self.settings.setValue('labelColor_pathogenic', color_pathogenic)#保存颜色设置
        self.settings.setValue('labelColorName_pathogenic', color_pathogenic.name())

    def getColor_GT(self):
        default_color_GT = QColor('#ecec00')#默认黄色
        color_GT = QColorDialog.getColor(default_color_GT)
        p_GT = QPalette()
        p_GT.setColor(QPalette.Window, color_GT)#Window是窗口，用于背景色设置，WindowText是文本，用于字体色设置
        self.ui.label_9.setAutoFillBackground(True)#是否填充背景，改文本颜色时要注掉或填False
        self.ui.label_9.setPalette(p_GT)
        self.ui.label_9.setText(color_GT.name())#颜色名称，用于传递给其他函数
        self.settings.setValue('labelColor_GT', color_GT)#保存颜色设置
        self.settings.setValue('labelColorName_GT', color_GT.name())

    def getColor_synonymous(self):
        default_color_synonymous = QColor('#ffff7f')#默认卡其
        color_synonymous = QColorDialog.getColor(default_color_synonymous)
        p_synonymous = QPalette()
        p_synonymous.setColor(QPalette.Window, color_synonymous)#Window是窗口，用于背景色设置，WindowText是文本，用于字体色设置
        self.ui.label_11.setAutoFillBackground(True)#是否填充背景，改文本颜色时要注掉或填False
        self.ui.label_11.setPalette(p_synonymous)
        self.ui.label_11.setText(color_synonymous.name())#颜色名称，用于传递给其他函数
        self.settings.setValue('labelColor_synonymous', color_synonymous)#保存颜色设置
        self.settings.setValue('labelColorName_synonymous', color_synonymous.name())

    def getColor_func(self):
        default_color_func = QColor('#ffaa00')#默认橘色
        color_func = QColorDialog.getColor(default_color_func)
        p_func = QPalette()
        p_func.setColor(QPalette.Window, color_func)#Window是窗口，用于背景色设置，WindowText是文本，用于字体色设置
        self.ui.label_13.setAutoFillBackground(True)#是否填充背景，改文本颜色时要注掉或填False
        self.ui.label_13.setPalette(p_func)
        self.ui.label_13.setText(color_func.name())#颜色名称，用于传递给其他函数
        self.settings.setValue('labelColor_func', color_func)#保存颜色设置
        self.settings.setValue('labelColorName_func', color_func.name())


    #——————————————第一次筛选表颜色设置——————————————————
    def getColor_eas_F(self):
        default_color_eas_F = QColor('#c2c2c2') #默认灰色
        color_eas_F = QColorDialog.getColor(default_color_eas_F)
        p_eas_F = QPalette()
        p_eas_F.setColor(QPalette.Window, color_eas_F)#Window是窗口，用于背景色设置，WindowText是文本，用于字体色设置
        self.ui.label_17.setAutoFillBackground(True)#是否填充背景，改文本颜色时要注掉或填False
        self.ui.label_17.setPalette(p_eas_F)
        self.ui.label_17.setText(color_eas_F.name())#颜色名称，用于传递给其他函数
        self.settings.setValue('labelColor_eas_F', color_eas_F)#保存颜色设置
        self.settings.setValue('labelColorName_eas_F', color_eas_F.name())
    
    def getColor_func_F(self):
        default_color_func_F = QColor('#ffff7f') #默认灰色
        color_func_F = QColorDialog.getColor(default_color_func_F)
        p_func_F = QPalette()
        p_func_F.setColor(QPalette.Window, color_func_F)#Window是窗口，用于背景色设置，WindowText是文本，用于字体色设置
        self.ui.label_19.setAutoFillBackground(True)#是否填充背景，改文本颜色时要注掉或填False
        self.ui.label_19.setPalette(p_func_F)
        self.ui.label_19.setText(color_func_F.name())#颜色名称，用于传递给其他函数
        self.settings.setValue('labelColor_func_F', color_func_F)#保存颜色设置
        self.settings.setValue('labelColorName_func_F', color_func_F.name())
    
    def getColor_OMIM(self):
        default_OMIM = QColor('#00ff00') #默认灰色
        color_OMIM = QColorDialog.getColor(default_OMIM)
        p_OMIM = QPalette()
        p_OMIM.setColor(QPalette.Window, color_OMIM)#Window是窗口，用于背景色设置，WindowText是文本，用于字体色设置
        self.ui.label_21.setAutoFillBackground(True)#是否填充背景，改文本颜色时要注掉或填False
        self.ui.label_21.setPalette(p_OMIM)
        self.ui.label_21.setText(color_OMIM.name())#颜色名称，用于传递给其他函数
        self.settings.setValue('labelColor_OMIM', color_OMIM)#保存颜色设置
        self.settings.setValue('labelColorName_OMIM', color_OMIM.name())


class mainwindow(QWidget):
    switch_window1 = pyqtSignal()
    switch_window2 = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()           
    def initUI(self):
        self.ui = uic.loadUi('./tools_select.ui')
        self.ui.setWindowIcon(QIcon('./logo2.ico'))
        self.ui.setWindowTitle('JXJY自动化工具选择')
        
        self.btn  = self.ui.pushButton
        self.btn2  = self.ui.pushButton_2
        self.btn.clicked.connect(self.go_appwindow)    
        self.btn2.clicked.connect(self.go_fengshi)    
    def go_appwindow(self):
        self.switch_window1.emit()
    def go_fengshi(self):
        self.switch_window2.emit()
        
    
class fengshiWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.ui = uic.loadUi('./.ui')
        self.ui.setWindowIcon(QIcon('./logo2.ico'))
        self.ui.setWindowTitle('JXJY自动化工具选择')
        self.ui.show()
        
        
        
#控制器，展示主界面以及用于跳转至其他页面
class Controller:
    def __init__(self):
        pass
    def MainShow(self):
        self.Main = mainwindow()
        self.Main.switch_window1.connect(self.AppShow)
        self.Main.switch_window2.connect(self.fengshiWindows)
        self.Main.ui.show()
    def AppShow(self):
        self.App = appwindow()
        #self.Main.ui.close()   #是否关闭主窗口
        self.App.ui.show()
    def fengshiWindows(self):
        self.FSapp = fengshiWindows()
        #self.Main.ui.close()   #是否关闭主窗口
        self.FSapp.ui.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    #启动界面
    splash = QSplashScreen(QPixmap("start2.jpg"))
    splash.show()
    splash.showMessage("启动中",Qt.AlignHCenter,Qt.red)
    app.processEvents()
    splash.finish(mainwindow())
    controller = Controller()   #控制器实例化
    controller.MainShow()       #默认展示mainwindow界面
    
    sys.exit(app.exec_())

