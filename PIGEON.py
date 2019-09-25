import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ntpath
import subprocess
import pipes

class PigeonApp(QTabWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PIGEON Client'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        #Menu bar and settings

        #Creating tabs
        self.HPC_tab =QWidget()
        self.addTab(self.HPC_tab,"HPC Account")
        self.run_sim_tab =QWidget()
        self.addTab(self.run_sim_tab,"Execute")
        self.render_tab=QWidget()
        self.addTab(self.render_tab,"Exodus viewer")
        self.csv_plot_tab=QWidget()
        self.addTab(self.csv_plot_tab,"Plot CSV")

        #Generating layouts for tabs
        self.hpc_UI()
        self.run_sim_UI()
        self.render_UI()
        self.csv_UI()

        ###DUMMY DATA --> REMOVE after testing
        self.dummy_data()

        #Main app window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('RAVEN_logo.png'))

        self.show()
        # self.initUI()


    def run_sim_UI(self):
        self.input_files = []

        layout=QGridLayout(self)
        layout.setSpacing(10)

        #Creating widgets
        self.get_files_button = (QPushButton('Select simulation files'))
        self.rem_files=(QPushButton('Remove selected file'))
        self.ip_files_list = QListWidget()                                  #Shows selected files
        self.HPC_run_dir=QLineEdit()
        self.HPC_run_dir_label = QLabel('HPC run directory location')
        self.NUM_PROCS=QLineEdit()
        self.n_name = QLabel('Number of processes')
        self.MEM_PER_PROC=QLineEdit()
        self.MEM_LABEL=QLabel('Memory per process')
        self.MEM_UNIT = QComboBox()
        self.JOB_TIME=QLineEdit()
        self.JOB_TIME_LABEL=QLabel('Job time on HPC')
        self.JOB_TIME_UNITS=QComboBox()
        self.JOB_NAME = QLineEdit()
        self.JOB_NAME_LABEL=QLabel('Job Name')

        self.RUN_SIMULATION  = (QPushButton('Run'))
        self.STOP_SIMULATION = (QPushButton('Stop'))
        self.execution_log_label = QLabel('Execution log')
        self.log_output = QTextEdit()
        self.burst_mode = QCheckBox("Burst mode")

        #Adding widgets on grid
        layout.addWidget(self.get_files_button,1,0)
        layout.addWidget(self.rem_files,2,0)
        layout.addWidget(self.ip_files_list,1,1,2,2)
        layout.addWidget(self.HPC_run_dir_label,3,0)
        layout.addWidget(self.HPC_run_dir,3,1)
        layout.addWidget(self.n_name,4,0)
        layout.addWidget(self.NUM_PROCS,4,1)
        layout.addWidget(self.burst_mode,4,2)
        layout.addWidget(self.MEM_LABEL,5,0)
        layout.addWidget(self.MEM_PER_PROC,5,1)
        layout.addWidget(self.MEM_UNIT,5,2)
        layout.addWidget(self.JOB_TIME_LABEL,6,0)
        layout.addWidget(self.JOB_TIME,6,1)
        layout.addWidget(self.JOB_TIME_UNITS,6,2)
        layout.addWidget(self.JOB_NAME_LABEL,7,0)
        layout.addWidget(self.JOB_NAME,7,1)
        layout.addWidget(self.RUN_SIMULATION,8,0)
        layout.addWidget(self.STOP_SIMULATION,8,1)
        layout.addWidget(self.execution_log_label,9,0)
        layout.addWidget(self.log_output,10,0,12,3)


        #Adding widget actions
        self.NUM_PROCS.setValidator(QIntValidator(bottom=0))
        self.get_files_button.clicked.connect(self.openFileNamesDialog)
        self.RUN_SIMULATION.clicked.connect(self.run_simulation)
        self.log_output.setReadOnly(True)
        self.MEM_UNIT.addItems(["MB","GB"])
        self.JOB_TIME_UNITS.addItems(["Min","Hours","Days"])
        self.run_sim_tab.setLayout(layout)

    def hpc_UI(self):
        layout=QGridLayout(self)
        layout.setSpacing(10)

        #creating widgets
        self.HPC_ac_name=QLineEdit()
        self.HPC_ac_name_label=QLabel('HPC Account Name')
        self.HPC_url=QLineEdit()
        self.HPC_url_label=QLabel('HPC URL')
        self.HPC_slurm_qos=QLineEdit()
        self.HPC_slurm_qos_label=QLabel("SLURM QOS")
        self.HPC_opt_loc=QLineEdit()
        self.HPC_opt_label=QLabel('HPC opt File')


        #Placing widgets on grid
        layout.addWidget(self.HPC_ac_name_label,1,0)
        layout.addWidget(self.HPC_ac_name,1,1)
        layout.addWidget(self.HPC_url_label,2,0)
        layout.addWidget(self.HPC_url,2,1)
        layout.addWidget(self.HPC_slurm_qos_label,3,0)
        layout.addWidget(self.HPC_slurm_qos,3,1)
        layout.addWidget(self.HPC_opt_label,4,0)
        layout.addWidget(self.HPC_opt_loc,4,1)

        #Extracting data from widgets
        # self.url = self.HPC_url.getText()
        self.HPC_tab.setLayout(layout)

    def dummy_data(self):
        #this function makes testing easier by setting default dummy dummy_data
        self.HPC_ac_name.setText('chaitanya.bhave')
        self.HPC_url.setText('hpg.rc.ufl.edu')
        self.HPC_slurm_qos.setText('michael.tonks')
        self.HPC_opt_loc.setText('~/projects/moose/modules/combined/combined-opt')

        self.setFilesDisplay(['~/projects/PIGEON_client/RUN_DIR/moose_inputfile.i'])
        self.HPC_run_dir.setText('/ufrc/michael.tonks/chaitanya.bhave/RAVEN/')
        self.NUM_PROCS.setText('2')
        self.MEM_PER_PROC.setText('200')
        self.JOB_TIME.setText('60')
        self.JOB_NAME.setText('TEST_JOB')

    def render_UI(self):
        layout=QGridLayout(self)
        layout.setSpacing(10)
        self.render_tab.setLayout(layout)
    def csv_UI(self):
        layout=QGridLayout(self)
        layout.setSpacing(10)
        self.csv_plot_tab.setLayout(layout)

    # def initUI(self):
    #
    #     self.window = QWidget()
    #     self.layout = QVBoxLayout()
    #     #Creating tabs
    #     # self.tabs=QTabWidget()
    #     self.tab1=QWidget()
    #     self.tab2=QWidget()
    #     self.addTab(self.tab1,"Run Simulation")
    #     self.addTab(self.tab2,"Render Simulation")
    #     # self.tabs.resize(self.width,self.height)
    #
    #     #Adding tabs to layout
    #     # self.layout.addWidget(self.tabs)
    #     # self.window.setLayout(self.layout)
    #     # self.tab1.setLayout(self.layout)
    #     #Creating display grid
    #     self.grid = QGridLayout(self)
    #     self.grid.setSpacing(10)
    #
    #
    #     #Creating widgets
    #     self.get_files_button = (QPushButton('Select simulation files'))
    #     self.rem_files=(QPushButton('Remove selected file'))
    #     self.ip_files_list = QListWidget()                                  #Shows selected files
    #     self.HPC_PATH=QLineEdit()
    #     self.HPC_PATH_name=QLabel('HPC run directory')
    #     self.NUM_PROCS=QLineEdit()
    #     self.NUM_PROCS.setValidator(QIntValidator(bottom=0))
    #     self.n_name = QLabel('Number of processes')
    #     self.RUN_SIMULATION  = (QPushButton('Run'))
    #     self.STOP_SIMULATION = (QPushButton('Stop'))
    #     self.RENDER_SIMULATION = (QPushButton('Render'))
    #     self.log_output = QTextEdit()
    #     self.render_scene = QGraphicsScene()
    #     self.render_view  = QGraphicsView()
    #
    #     #Adding items on grid
    #     self.grid.addWidget(self.get_files_button,1,0)
    #     self.grid.addWidget(self.rem_files,2,0)
    #     self.grid.addWidget(self.ip_files_list,1,1,2,2)
    #     self.grid.addWidget(self.HPC_PATH_name,3,0)
    #     self.grid.addWidget(self.HPC_PATH,3,1)
    #     self.grid.addWidget(self.n_name,4,0)
    #     self.grid.addWidget(self.NUM_PROCS,4,1)
    #     self.grid.addWidget(self.RUN_SIMULATION,5,0)
    #     self.grid.addWidget(self.STOP_SIMULATION,5,1)
    #     self.grid.addWidget(self.RENDER_SIMULATION,5,2)
    #     self.grid.addWidget(self.log_output,6,0,10,2)
    #     # self.grid.addWidget(self.render_view,1,3,6,6)
    #     # self.HPC_PATH, _ =QInputDialog.getText(self,"Get Path","Type HPC run director path")
    #     #Setting actions
    #     self.get_files_button.clicked.connect(self.openFileNamesDialog)
    #     self.RUN_SIMULATION.clicked.connect(self.run_simulation)
    #     self.log_output.setReadOnly(True)
    #
    #     #Setting locations
    #     # self.rem_files.move(0,50)
    #     # self.ip_files_list.move(200,0)
    #     # self.HPC_form.move(0,150)
    #
    #     # self.HPC_PATH.move(0,100)
    #
    #     #Setting important variables
    #     self.input_files = []
    #     # self.openFileNameDialog()
    #     # self.openFileNamesDialog()
    #     # self.saveFileDialog()
    #     self.setLayout(self.grid)

#Widget action functions
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        self.setFilesDisplay(files)

    def setFilesDisplay(self,files):
        if files:
            update_items=list(set(files) - set(self.input_files))
            self.input_files+=files
            self.input_files = list(set(self.input_files))
            for filepath in update_items:
                filename=ntpath.basename(filepath)
                self.ip_files_list.addItem(filename)

    def run_simulation(self):
        ip_file = [file for file in self.input_files if file[-2:]=='.i' ]
        if not len(ip_file) >= 1:
            self.log_output.textCursor().insertHtml("<b><font color =\"red\">There should be atleast one input file file with a '.i' extension<br></font></b>")
            self.log_output.moveCursor(QTextCursor.End)
            #for multiple .i files must ask which is master .i file
        else:
            host=self.HPC_url.text()
            acct=self.HPC_ac_name.text()

            self.log_output.textCursor().insertHtml("Checking if HPC account and directory path exist<br>")
            self.log_output.moveCursor(QTextCursor.End)
            #Check that the path exists on HPC
            ssh_host = acct+'@'+host
            temp=self.exists_remote(ssh_host,self.HPC_run_dir.text())
            print("Status: ",temp)
            if not(temp):
                self.log_output.textCursor().insertHtml("Given directory does not exist on HPC. Please check HPC account details and directory path<br>")
                return
            self.log_output.textCursor().insertHtml("HPC account and path verified. Creating job folder and copying required files<br>")

    #         # cmd = "sbatch -n 2 " + self.HPC_PATH.text()+'/'+'init_paraview.sh'
    #         self.log_output.textCursor().insertHtml("ssh "+ssh_cmd)
    #         #
            # ssh=subprocess.Popen(["ssh","%s" % host, cmd ], shell=False,
            #            stdout=subprocess.PIPE,
            #            stderr=subprocess.PIPE)
            # result = ssh.stdout.readlines()
            # if result == []:
            #     error = ssh.stderr.readlines()
            #     print (sys.stderr, "ERROR: %s" % error)
            # else:
            #     print (result)
            # print(run_cmd)

    def exists_remote(self,host, path):
        """Test if a file exists at path on a host accessible with SSH."""
        cmd = "if [ -d " +path + " ]; then echo '1'; else echo '0'; fi"
        print(cmd)

        status = subprocess.call(
            ['ssh', host, cmd])
        return status
        raise Exception('SSH failed')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RavenApp()
    sys.exit(app.exec_())
