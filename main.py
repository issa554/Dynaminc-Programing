import tkinter as tk
from tkinter import ttk ,filedialog ,messagebox 
import random
import sys

#make function that Read the DP table and return the result
def print_lcs(b, y, i, j, result ):
    if i == 0 or j == 0:
        return
    elif b[i][j] == '\\':
        print_lcs(b, y, i - 1, j - 1, result)
        result.append(y[j - 1]) # he add the number of leds only when arrow is \
    elif b[i][j] == '|':
        print_lcs(b, y, i - 1, j, result)
    else:
        print_lcs(b, y, i, j - 1, result)

#the main function of program that write the DP table
def run_action(value ,leds ):
    count = 0;
    x = [1 + i for i in range(value)] # make an array that have number from 1 to the last number of led
    y = leds
    c = [[0] * (len(y) + 1) for _ in range(value + 1)] #make 2D array to have the number of leds can turn
    b = [[''] * (len(y) + 1) for _ in range(value + 1)]#make 2D array of arrows

    dp_box.delete("all")    # Delete all content on DP table
    dp_box.configure(scrollregion=(0,0,(value*55),(value*62))) #make scroll dynamic
    for i in range(len(leds)) :
        dp_box.create_text(((i+1)*(50)), (50), text=leds[i], fill="black" )
        dp_box.create_text(10, ((i+2)*(50)), text=i+1, fill="black")

# Cheak if the leds in y and x is == or what
    for i in range(1, value + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = '\\'
            elif c[i][j - 1] > c[i - 1][j]:
                c[i][j] = c[i][j - 1]
                b[i][j] = '-'
            else:
                c[i][j] = c[i - 1][j]
                b[i][j] = '|'
            dp_box.create_text(((j)*(50)), ((i+1)*(50)), text=(b[i][j]+"\n"+str(c[i][j])), fill="black") #print the arrow in screen
            count = c[i][j]  # to know the bigger number can turn
#XY    

    result = []
    print_lcs(b, y, value, len(y), result) # call print_lcs
    res_LEDS_field.config(state="normal")
    res_LEDS_field.delete("1.0", tk.END)    # Delete all text content
    res_LEDS_field.insert(tk.END,result)
    res_LEDS_field.config(state="disabled")

    res_field.config(text=count) #print the number of turn leds in field
    draw_leds(y , result) # call draw leds
   
# Find if there miss number in file   
def miss_number(size , C): #by use the bits array we created
    for i in range(1,size+1):      
        byteNumber = i // 8
        bitNumber = 7 - i % 8
        if (C[byteNumber] & (1 << bitNumber)) == 0:
            messagebox.showerror("NumericError",f"Number {i} is miss.") 
            return         

#make a function to get data from file
def read_file():
     #get the file
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])
    
    if file_path:
        num_array = []  # Initialize an empty list to store int for leds
        with open(file_path, 'r') as file:
            words =[] # make an  array to can read line by line
            first_int = 0
            line = file.readline()
            words = line.split()
            if len(words) ==0 : # get the first number that will be the size of leds and confirm it is valid number
                       messagebox.showerror("NumericError","Empty file")
                       return
            if not words[0].isdigit():
                       messagebox.showerror("NumericError",f"Non-numeric not accept or negative ->{words[0]}")
                       return
            if  int(words[0]) > 900:
                       messagebox.showerror("NumericError",f"max number you can use is 900")
                       return
            
            first_int = int(words[0])
            byteNumber = first_int // 8
            C = bytearray(byteNumber+1) #Make an array of bytes to can use a bit
            

            for line in file : # read a line and put inside into array 
                num = line.split()
                words.extend(num)
            count = 1
            #make a loop to cheak the all number of file if it Vaild
            while count <= first_int:     
                if  count >= len(words): #if not all number is there
                        miss_number(first_int,C)
                        return
                if not words[count].isdigit():#if it digit or string
                       messagebox.showerror("NumericError",f"Non-numeric not accept or negative ->{words[count]}")
                       return
                if int(words[count]) > first_int : #the system sholdn't have number biggter then size
                       messagebox.showerror("NumericError",f"Number {words[count]} is bigger then {first_int}")
                       return
                byteNumber = int(words[count]) // 8
                bitNumber = 7 - int(words[count]) % 8
                if (C[byteNumber] & (1 << bitNumber)) != 0: # if number is repeated
                        messagebox.showerror("NumericError",f"Number {words[count]} is repeated.") 
                        return 
                else:
                    C[byteNumber] = C[byteNumber] | (1 << bitNumber)
                num_array.append(int(words[count]))
                count += 1     
            run_action(first_int,num_array) #call run function      

#make a function to get data from user
def read_input() :
#make a new Screen for this window
    inpu = tk.Tk()
    inpu.geometry("500x500+300+120")
    inpu.title("Input leds")
    inpu.configure(bg="#dee2ff")
    # item  grid
    InFrame = tk.Frame(inpu , bg="#dee2ff" )
    InFrame.pack(pady=10)
    numberINp = tk.Entry(InFrame )
    numberINp.grid(column= 0 ,row=0)
    number = tk.Entry(InFrame )
    number.grid(column= 0 ,row=1)
    x=[] #make an array to have item of leds
    def setBTNs ():#when user chose the number of leds he will write
        if(numberINp.get().isdigit() and int(numberINp.get()) > 0 ): #confitm that the number is valid
            btn.configure(state="disabled")
            numberINp.configure(state="disabled")
            global size
            size=int(numberINp.get())
            global C
            byteNumber = size // 8
            C = bytearray(byteNumber+1) #make array of bytes to can use bit
            number.configure(state="normal")
            ADDbtn.configure(state="normal")
            Restbtn.configure(state="normal")
           
        else:
            messagebox.showerror("NumericError","Enter Valid number Only")
            return
    def ADDBTNs():#when user enter led by led
        num_box.configure(state="normal")
        num = number.get()
        number.delete(0, "end") #clear the led number field
        if not num.isdigit():#make a list of cheak for validtion
            messagebox.showerror("NumericError",f"Non-numeric not accept or negative ->{num}")
            return
        if int(num) > size :
            messagebox.showerror("NumericError",f"Number {num} is bigger then {size}")
            return
        if int(num) == 0  :
            messagebox.showerror("NumericError","Zero is inValid")
            return
        byteNumber = int(num) // 8
        bitNumber = 7 - int(num) % 8
        if (C[byteNumber] & (1 << bitNumber)) != 0:
                        messagebox.showerror("NumericError",f"Number {num} is repeated.") 
                        return 
        else:
            C[byteNumber] = C[byteNumber] | (1 << bitNumber)
            num_box.insert(tk.END,num+" ")
            x.insert(len(x),int(num) )
            num_box.configure(state="disabled")

        if(len(x) == size):
            RUNbtn.configure(state="normal")
            num_box.configure(state="disabled")
            ADDbtn.configure(state="disabled")
            number.configure(state="disabled")
             

    ADDbtn = tk.Button(InFrame , text="Add Number" , command=ADDBTNs)
    ADDbtn.grid(column=1 , row=1)
    number.configure(state="disabled")
    ADDbtn.configure(state="disabled")
    num_box = tk.Text(InFrame, height=60, wrap=tk.WORD, state="disabled", width=20)
    num_box.grid(column=0 , row=2)

    def run():
        run_action(size ,x)   #call the run function when btn run click
        
    btn = tk.Button(InFrame , text="Set Size" , command=setBTNs)
    btn.grid(column=1 , row=0)
    RUNbtn = tk.Button(InFrame , text="RUN" , command=run, state="disabled")
    RUNbtn.grid(column=2 , row=0)

    def rest(): #the rest function that clear all data the user enter
        RUNbtn.configure(state="disabled")
        btn.configure(state="normal")
        numberINp.configure(state="normal")
        numberINp.delete(0, tk.END)
        RUNbtn.configure(state="disabled")
        ADDbtn.configure(state="disabled")
        number.configure(state="disabled")
        number.configure(state="disabled")
        ADDbtn.configure(state="disabled")
        num_box.configure(state="normal")
        num_box.delete("1.0", tk.END)
        num_box.configure(state="disabled")
        size = 0
        x.clear()
        C.clear()

    Restbtn = tk.Button(InFrame , text="Rest" ,width=20, command=rest , bg="red",state="disabled" )
    Restbtn.grid(column=3 , row=0)

#make a function make random array of numbers
def randomnum() :
   #make a new window
    Random = tk.Tk()
    Random.geometry("300x200+500+200")
    Random.title("Random Number")
    Random.configure(bg="#ef233c")
    #lo
    InFrame = tk.Frame(Random , bg="#ef233c" )
    InFrame.pack(pady=50)
    numberINp = tk.Entry(InFrame  )
    numberINp.grid(column= 0 ,row=0)

    def run():
        if(numberINp.get().isdigit() and int(numberINp.get()) > 0 ): #cofirm that the number user enter is vaild
            if(int(numberINp.get()) > 500 ):
                messagebox.showerror("NumericError","Max number for random is 500")
                return 
            global size
            size=int(numberINp.get())
            # Generate an array of unique random integers
            global random_numbers
            random_numbers = random.sample(range(1, size + 1), size)          
        else:
            messagebox.showerror("NumericError","Enter Valid number Only")
            return
        run_action(size ,random_numbers)   #call run function
    runbtn = tk.Button(InFrame , text="Run " , command=run, cursor="hand2" , border=4 , bg="#e0e1dd")
    runbtn.grid(column=2 , row=0)    

#the function that draw leds in screen
def draw_leds(leds , res) :

    # Clear all things in draw screen and make scroll is daynamic
    canvas.delete("all")
    canvas.configure(scrollregion=(0,0,400,max(800,(110*len(leds)))))   
    #make an byte array to can know the leds will turn or not
    byteNumber = len(leds) // 8
    C = bytearray(byteNumber+1)
    for i in range(len(res)): #Search for turns leds and put number 1 in here place
        byteNumber = int(res[i]) // 8
        bitNumber = 7 - int(res[i]) % 8
        C[byteNumber] = C[byteNumber] | (1 << bitNumber)          
    count = 0
    for led in leds :
        byteNumber = int(led) // 8
        bitNumber = 7 - int(led) % 8
        if (C[byteNumber] & (1 << bitNumber)) != 0: #if the leds is turn put the image have turn led and the wire
           canvas.create_image(10, count*105, anchor=tk.NW, image=on)
           canvas.create_line(135, (count+1)*105-53, 300, (int(led))*105-53, fill="red", width=2)
#X1,Y1,X2,Y2        
        else: #else put off image
            canvas.create_image(10, count*105, anchor=tk.NW, image=off)
        canvas.create_image(300, count*105, anchor=tk.NW, image=battery) #put the battery image

        canvas.create_text(50, (count+1)*105-53, text=led, fill="black") # write the number of led and battery on screen
        canvas.create_text(325, (count+1)*105-53, text=count+1, fill="white")
        count+=1
     
def on_closing():
     sys.exit()     
# Create the main window
root = tk.Tk()
root.title("Project #1 Dynaminc Programing")
root.geometry("500x500")
root.state('zoomed')  #make screen full
root.protocol("WM_DELETE_WINDOW", on_closing)


# Create a frame for the left section
left_frame = tk.Frame(root, bg="#85c7de")
left_frame.grid(row=0, column=0, padx=0, pady=0,  sticky="nsew")
left_frame.columnconfigure(0, weight=1)
left_frame.rowconfigure(0, weight=1)

# Create a frame for the right section
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

# make the frames expand with the window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create a frame for output field
frame = tk.Frame(left_frame, padx=20,pady=20  , height=150 ,bg="#85c7de" )
frame.place(in_=left_frame, anchor="c", relx=.5, rely=.2)


result_label = ttk.Label(frame, text="Result:" , background="#85c7de")
res_field = ttk.Label(frame , text="" , background="#85c7de")

result_LEDS_label = ttk.Label(frame, text="LEDs will turn:" , background="#85c7de")
res_LEDS_field = tk.Text(frame,height=5, width=60 , state="disabled" , background="#85c7de")

# Create frame for DP table
dp_frame = tk.Frame(left_frame)
dp_frame2 = tk.Frame(dp_frame , height=500)
dp_frame2.pack(side="bottom" , fill="both")#make 2 frame to can put 2 scrollbar
dp_box = tk.Canvas(dp_frame2, height=300, width=500 ,bg="#85c7de",scrollregion=(0, 0, 1400, 600)) #make canvas for dp table

scrollbar = tk.Scrollbar(dp_frame2, command=dp_box.yview ) #Scrollbar for dp in y-axis
dp_box.configure(yscrollcommand=scrollbar.set)

horizontal_scrollbar = tk.Scrollbar(dp_frame, command=dp_box.xview, orient=tk.HORIZONTAL)#Scrollbar for dp in x-axis
dp_box.configure(xscrollcommand=horizontal_scrollbar.set)

# Pack the Scrollbar 
dp_box.pack(side="left", fill="both", expand=True)
horizontal_scrollbar.pack(side="top", fill="x")
scrollbar.pack(side="right", fill="y")

# Create a buttons for file , input and random
read_button = tk.Button(frame, text="Read From File", command=read_file , bg="#cfe8ef" , border=4,cursor="hand2")
from_input = tk.Button(frame, text="Read From Input", command=read_input , bg="#cfe8ef", border=4,cursor="hand2")
from_random = tk.Button(frame, text="Random ", command=randomnum , bg="#cfe8ef", border=4,cursor="hand2")


# Add labels and text fields to the frame
read_button.grid(column=0, row=0, sticky=(tk.W, tk.E))
from_input.grid(column=1, row=0, sticky=(tk.W, tk.E))
from_random.grid(column=2, row=0, sticky=(tk.W, tk.E))

result_LEDS_label.grid(column=0, row=3, sticky=tk.W)
res_LEDS_field.grid(column=1, row=3, sticky=(tk.W, tk.E))

result_label.grid(column=0, row=2, sticky=tk.W)
res_field.grid(column=1, row=2, sticky=(tk.W, tk.E))

dp_frame.grid(column=0, row=4, sticky=(tk.W, tk.E))

#create a canvas for draw leds
canvas = tk.Canvas(right_frame, width=200, bg="#00b4d8",height=1000 ,scrollregion=(0, 0, 400, 1000))
canvas.pack(side="left", fill="both", expand=True)
scroll_bar = ttk.Scrollbar(right_frame , orient="vertical" , command=canvas.yview)
scroll_bar.pack(side="left" ,fill=tk.Y)
canvas.configure(yscrollcommand=scroll_bar.set)
canvas.bind("<Configure>", lambda e :canvas.configure(scrollregion=canvas.bbox("all")))
#define the images we will use for leds
on = tk.PhotoImage(file='on.png') 
battery = tk.PhotoImage(file='battery.png') 
off = tk.PhotoImage(file='off.png') 
# Run the Tkinter event loop
root.mainloop()