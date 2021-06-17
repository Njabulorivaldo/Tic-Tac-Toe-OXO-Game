from GameClient import *

class OXOTextClient(GameClient):

    def __init__(self):
        GameClient.__init__(self)
        self.board = [' '] * BOARD_SIZE
        self.shape = None
        
    def clear_board(self):
        self.board = [' '] * BOARD_SIZE
        
    def input_server(self):
        return input('enter server:')
     
    def input_move(self):
        return input('enter move(0-8):')
     
    def input_play_again(self):
        return input('play again(y/n):')

    def display_board(self):
        board_copy = self.board
        for i in range(3):
            print("|", end='')
            for n in board_copy[:3]:
                print("{:^3}".format(n), end='|')
            print()
            board_copy = board_copy[3:]        
    
    def handle_message(self,msg):
        
        #=====introduces a new game and assign each player a character shape=====
        if msg[:msg.find(",")] == "new game":
            print("New Game!!, Your character is: ",msg[-1],"\n") 
            self.display_board() #displays the board
        
        #=====tells a player it's their turn to play and allow them to make a move======
        elif msg == "your move":
            print("It is your turn, make a move!\n")
            move = self.input_move() #gets the players move
            self.send_message(move) #sends a message to the server
        
        #==========Notifies the player about their opponents move========
        elif msg == "opponents move": 
            print("Opponents move\n")
        
        #=====slices the message and gets the shape and position=========
        elif msg[:msg.find(",")] == "valid move":
            shape = msg[-3] #gets the shape of the move made
            pos = int(msg[-1]) #gets the position
            self.board[pos] = shape #adds the shape to the board
            self.display_board() #Displays the updated board
        
        elif msg == "invalid move":
            print("Invalid move!, Enter a valid move!")
        
        #========Displays the results of the game========
        elif msg[:msg.find(",")] == "game over":
            shape = msg[-1]
            if shape == "T":
                print("Game over, it is a tie\n")
            else:
                print("Game over, the winner is: "+ shape+"\n")
     
        #=====asks for a remath and sends the responses of the players to the server======
        elif msg == "play again":
            resp = self.input_play_again()
            if resp == "y":
                self.send_message(resp) #sends the response to the server
                self.clear_board() #clears the board for a new game to begin
            else:
                self.send_message("n")
                print("You left the game!\n")
                
        #==========The game if exited at this point=========
        elif msg == "exit game":
            print("Player left the game")
            
    def play_loop(self):
        while True:
            msg = self.receive_message()
            if len(msg): self.handle_message(msg)
            else: break
            
def main():
    otc = OXOTextClient()
    while True:
        try:
            otc.connect_to_server(otc.input_server())
            break
        except:
            print('Error connecting to server!')
    otc.play_loop()
    input('Press click to exit.')
        
main()