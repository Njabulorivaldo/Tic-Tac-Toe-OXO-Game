import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from GameClient import *

class Playloop(QThread, GameClient):
    msg_sig = pyqtSignal(str) #signal
    
    def __init__(self): #constructor
        QThread.__init__(self)
        GameClient.__init__(self)
        
        
    def host_name(self, host):
        '''
        Connects the user to the server and tell them they are connected through the server messages widget and clears the board for the game or tell them if they are not connected. 
        '''
        
        while True:
            try:    
                self.connect_to_server(host)
                break
            except:
                return
        
        
    def run(self):
        '''
        This is the play loop for the game
        '''
        while True :
            msg = self.receive_message()
            if len(msg): self.msg_sig.emit(msg)
            
            
    def get_input(self, move):

        
        self.send_message(move)
        
        
        
        
class Game(QWidget, GameClient):
    
    def __init__(self): #constructor
        QWidget.__init__(self)
        GameClient.__init__(self)
        self.setGeometry(250,250,750,750)
        self.setWindowTitle("OXO GAME")
        self.setWindowIcon(QIcon('logo.png'))
        self.game_layout()
        
        self.loop = Playloop()
        self.loop.msg_sig.connect(self.handle_message)  #connects the signal with the handle_messages method
        
    def colors(self):
        '''
        Changes the background of the window if executed according to the selected color in the the combobox
        '''
        if self.col_combo.currentText() == 'Green':     #green background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.green)
            self.setPalette(bg_color) 
        if self.col_combo.currentText() == 'Cyan':     #cyan background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.cyan)
            self.setPalette(bg_color)    
        if self.col_combo.currentText() == 'Yellow':     #yellow background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.yellow)
            self.setPalette(bg_color)    
        if self.col_combo.currentText() == 'White':     #no coloured background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.white)
            self.setPalette(bg_color)    
            
        if self.col_combo.currentText() == 'Gray':     #gray background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.gray)
            self.setPalette(bg_color)    
            
        
    def gui_new_game(self):
        '''
        clears the board by updating the board with blank images.
        '''
        self.shape1.setPixmap(QPixmap('blank.gif'))
        self.shape2.setPixmap(QPixmap('blank.gif'))
        self.shape3.setPixmap(QPixmap('blank.gif'))
        self.shape4.setPixmap(QPixmap('blank.gif'))
        self.shape5.setPixmap(QPixmap('blank.gif'))
        self.shape6.setPixmap(QPixmap('blank.gif'))
        self.shape7.setPixmap(QPixmap('blank.gif'))
        self.shape8.setPixmap(QPixmap('blank.gif'))
        self.shape9.setPixmap(QPixmap('blank.gif'))  
        
        
    def host_name(self):
        '''
        Gets the current server name entered in the line edit and make connection
        Caters for localhost only
        '''
        if self.con_host.text() == 'localhost':
            self.loop.host_name(self.con_host.text())
            self.loop.start() 
            
        else:
            self.listwidget.addItem("Error connecting to this server!")
        
        
    def handle_message(self, msg):
        '''
        Receives the message from the server and handles it according to it's category
        '''
        
        if msg[:msg.find(",")] == "new game":
            self.listwidget.addItem("Connected") #shows connection
            self.listwidget.addItem("New Game, your shape is shown on the left")
            #sets the shape on the left for the player
            if msg[-1] == "X":
                self.shape.setPixmap(QPixmap("cross.gif"))
            else:
                self.shape.setPixmap(QPixmap("nought.gif"))
                
        elif msg == "your move":
            self.listwidget.addItem("Your move")
            self.play_button.clicked.connect(self.user_move)
            
        elif msg == "opponents move":
            self.listwidget.addItem("Opponent's move")
            
        elif msg[:msg.find(",")] == "valid move":
            #adds the player's move to the board
            shape = msg[-3]
            pos = int(msg[-1])
            if msg[-3] == "O":
                self.shapes_list[pos].setPixmap(QPixmap('nought.gif'))
            else:
                self.shapes_list[pos].setPixmap(QPixmap('cross.gif'))
            
        elif msg == "invalid move":
            self.listwidget.addItem("Invalid move")
            
        elif msg[:msg.find(",")] == "game over":
            #Displays the winner in a dialog box or shows a messagebox if it is a draw game
            win_dialog = QDialog(self)
            win_dialog.setWindowTitle("WINNNER")
            b1 = QPushButton("ok",win_dialog)
            b1.move(50,50)
            b1.clicked.connect(win_dialog.close)
            if msg[-1] == "T": #Draw game
                QMessageBox.about(self, "Match Results", "Match is a Draw\n     !!!!!")
            elif msg[-1] == "O":
                self.winner = QLabel(win_dialog) 
                pixmap = QPixmap('nought.gif')
                self.winner.setPixmap(pixmap)
                self.resize(pixmap.width(),pixmap.height())  
                self.winner.move(70,0)
                win_dialog.exec()            
            else: 
                self.winner = QLabel(win_dialog) 
                pixmap = QPixmap('cross.gif')
                self.winner.setPixmap(pixmap)
                self.resize(pixmap.width(),pixmap.height())  
                self.winner.move(70,0)
                win_dialog.exec()            
            
        elif msg == "play again":
            #connects the button called new game for a new game to occur to the play again method
            self.new_game.clicked.connect(self.play_again)
        elif msg == "exit game":
            self.listwidget.addItem("Player left the game")
            self.exit_button.clicked.connect(self.no_newgame) 
            
        
    def play_again(self):
        '''
        Executes if the user clicked the new game button after a completed game and clears the server messages then disconnects the button to avoid interuption from the button
        '''
        self.loop.get_input("y")
        self.gui_new_game()
        self.listwidget.clear() #clears the finished game server messages
        self.new_game.clicked.disconnect(self.play_again) 
        
    def user_move(self):
        '''
        Gets the user's move and pass it to the Playloop thread and clears line edit for a new move
        then disconnects the button to avoid interuptions
        '''
        move = self.player_move.text()
        self.loop.get_input(move)
        self.player_move.clear() 
        self.play_button.clicked.disconnect(self.user_move)
        
    def close_button(self):
        '''
        Executes if the exit button is clicked and asks the user if they really want to exit the game 
        '''
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()    #exits the game
            
        else:
            pass #pass the message and returns to the game
        
    def no_newgame(self):
        self.loop.get_input("n")
        
    def help(self):
        '''
        Executes when the user clicks the help button and show them the possible moves in the game
        with a dialogue box containing a help image
        '''
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("WINNNER")
        b1 = QPushButton("ok",help_dialog)
        b1.move(100,200)
        b1.clicked.connect(help_dialog.close)  
        
        pic = QLabel(help_dialog) 
        pixmap = QPixmap('help.png')
        pic.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())  
        pic.move(70,0)
        help_dialog.exec()   
        
    def game_layout(self):
        '''
        This is the GUI interface
        '''
        principal_layout = QGridLayout() #final layout of the window
        
        #initial background color for the game
        self.setAutoFillBackground(True)
        bg_color = self.palette()
        bg_color.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(bg_color)
        
        #=====connection widgets=====
        
        con_label = QLabel("Server: ")
        self.con_host = QLineEdit(self)
        con_button = QPushButton("CONNECT")
        con_button.clicked.connect(self.host_name)
        
        #adding the connection widgets to the final layout
        principal_layout.addWidget(con_label, 0, 2)
        principal_layout.addWidget(self.con_host, 0, 3, 1, 4)
        principal_layout.addWidget(con_button, 0, 7)
        
        #=========color change widgets============
        
        col_label = QLabel("Game Color: ")
        self.col_combo = QComboBox()
        self.col_combo.addItems(["Gray", "Green", "Cyan", "Yellow", "White"])
        col_button = QPushButton("CHANGE")
        col_button.clicked.connect(self.colors)
        
        #adding the color change widgets to the final layout
        principal_layout.addWidget(col_label, 1, 2)
        principal_layout.addWidget(self.col_combo, 1, 3, 1, 4)
        principal_layout.addWidget(col_button, 1, 7)
        
        #==========shape of the player===========
        
        shape_box = QGroupBox("Your Shape")
        self.shape = QLabel(self) 
        pixmap = QPixmap('blank.gif')
        self.shape.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height()) 
        
        #adding the shape into the box on the window
        box = QVBoxLayout()
        box.addWidget(self.shape)
        shape_box.setLayout(box)
        
        #adding the shape to the final layout
        principal_layout.addWidget(shape_box, 2, 0, 1, 2)        
       
        #=========server messages=================
        
        serv_box = QGroupBox("Server Messages")
        sv = QGridLayout()
        sv_box = QGroupBox("Server Messages")
        self.listwidget = QListWidget()
        sv.addWidget(self.listwidget, 0, 0)
        sv_box.setLayout(sv)
     
        principal_layout.addWidget(sv_box, 2, 2, 2, 8)
        
        #===============shapes of the board================
        
        self.shape1 = QLabel(self) 
        pixmap = QPixmap('blank.gif')
        self.shape1.setPixmap(pixmap)
       
        self.shape2 = QLabel(self) 
        pixmap = QPixmap('blank.gif')
        self.shape2.setPixmap(pixmap)
        
        self.shape3 = QLabel(self) 
        pixmap = QPixmap('blank.gif')
        self.shape3.setPixmap(pixmap)

        self.shape4 = QLabel(self) 
        pixmap = QPixmap('blank.gif')
        self.shape4.setPixmap(pixmap)
        
        self.shape5 = QLabel(self) 
        pixmap = QPixmap('blank.gif')
        self.shape5.setPixmap(pixmap)

        self.shape6 = QLabel(self) 
        pixmap = QPixmap('blank.gif')
        self.shape6.setPixmap(pixmap)
        
        self.shape7 = QLabel(self) 
        pixmap = QPixmap('blank.gif')
        self.shape7.setPixmap(pixmap)

        self.shape8 = QLabel(self) 
        pixmap = QPixmap('blank.gif')
        self.shape8.setPixmap(pixmap)
        
        self.shape9 = QLabel(self) 
        pixmap = QPixmap('blank.gif')
        self.shape9.setPixmap(pixmap)        
        
        #===========board game=================== 
        
        play_box = QGroupBox()
        self.shapes_list = [self.shape1, self.shape2, self.shape3, self.shape4,
                       self.shape5,self.shape6, self.shape7, self.shape8, self.shape9]
        
        #adding shapes to the board
        play_grid = QGridLayout()
        play_grid.addWidget(self.shapes_list[0], 0, 0)
        play_grid.addWidget(self.shapes_list[1], 0, 1)
        play_grid.addWidget(self.shapes_list[2], 0, 2)
        play_grid.addWidget(self.shapes_list[3], 1, 0)
        play_grid.addWidget(self.shapes_list[4], 1, 1)
        play_grid.addWidget(self.shapes_list[5], 1, 2)
        play_grid.addWidget(self.shapes_list[6], 2, 0)
        play_grid.addWidget(self.shapes_list[7], 2, 1)
        play_grid.addWidget(self.shapes_list[8], 2, 2)
        
        #adding the board game to the final layout
        play_box.setLayout(play_grid)
        principal_layout.addWidget(play_box, 5, 2, 2, 8)
        
        
        #=================Play and help Area==============
        
        self.player_move = QLineEdit()
        self.play_button = QPushButton("PLAY")
        help_button = QPushButton("help")
        help_button.clicked.connect(self.help)
        
        
        principal_layout.addWidget(self.play_button, 8, 5, 2, 3)
        principal_layout.addWidget(self.player_move, 8, 2, 2, 3)
        principal_layout.addWidget(help_button, 8, 8, 2,1)
        
        
        #=========play again and Exit buttons=========
        
        self.new_game = QPushButton("NEW GAME")
        self.exit_button = QPushButton("EXIT")
        self.exit_button.clicked.connect(self.close_button) 
        
        #adding the buttons to the final layout
        principal_layout.addWidget(self.new_game, 10, 1)
        principal_layout.addWidget(self.exit_button, 10, 9)
        
        #displaying the final layout
        self.setLayout(principal_layout)    
    
def main():
    app = QApplication(sys.argv)
    window = Game() 
    window.show()
    sys.exit(app.exec_())
   
main()