# Creator: Thomas Cowie
# Context: Sort visualiser app with a login, quiz, and sorting animations. I made this for my OCR A-level Computer science Coursework.
# Credit: The sorting animations were adapted from the github user "nrsyed"
# Credit: Github repo from "nrsyed": https://github.com/nrsyed/sorts/tree/master"

#imports
from tkinter import *
from tkinter import PhotoImage, messagebox
import sqlite3
import hashlib
import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  

# Helper function to swap elements i and j of list A
def swap(A, i, j):
    if i != j:
        A[i], A[j] = A[j], A[i]

#function that carrys out a bubble sort on a data set "A"
def bubblesort(A):
    if len(A) == 1:
        return
    swapped = True
    for i in range(len(A) - 1):
        if not swapped:
            break
        swapped = False
        for j in range(len(A) - 1 - i):
            if A[j] > A[j + 1]:
                swap(A, j, j + 1)
                swapped = True
            yield A
#function that carrys out a Insertion sort on a data set "A"
def insertionsort(A):
    for i in range(1, len(A)):
        j = i
        while j > 0 and A[j] < A[j - 1]:
            swap(A, j, j - 1)
            j -= 1
            yield A
#function that carrys out a Merge sort on a data set "A"
def mergesort(A, start=0, end=None):
    if end is None:
        end = len(A) - 1
    if start < end:
        mid = (start + end) // 2
        yield from mergesort(A, start, mid)
        yield from mergesort(A, mid + 1, end)
        yield from merge(A, start, mid, end)
        yield A
#Helper function that merges two sorted subarrays of a list into a single sorted segment
def merge(A, start, mid, end):
    merged = []
    leftIdx = start
    rightIdx = mid + 1
    while leftIdx <= mid and rightIdx <= end:
        if A[leftIdx] < A[rightIdx]:
            merged.append(A[leftIdx])
            leftIdx += 1
        else:
            merged.append(A[rightIdx])
            rightIdx += 1
    while leftIdx <= mid:
        merged.append(A[leftIdx])
        leftIdx += 1
    while rightIdx <= end:
        merged.append(A[rightIdx])
        rightIdx += 1
    for i, sorted_val in enumerate(merged):
        A[start + i] = sorted_val
        yield A
#Function that carrys out a quick sort on a data set "A"
def quicksort(A, start, end):
    if start >= end:
        return
    pivot = A[end]
    pivotIdx = start
    for i in range(start, end):
        if A[i] < pivot:
            swap(A, i, pivotIdx)
            pivotIdx += 1
        yield A
    swap(A, end, pivotIdx)
    yield A
    yield from quicksort(A, start, pivotIdx - 1)
    yield from quicksort(A, pivotIdx + 1, end)

#Function that updates the animations
def update_fig(A, rects, iteration, text):
    for rect, val in zip(rects, A):
        rect.set_height(val)
    iteration[0] += 1
    text.set_text(f"# of operations: {iteration[0]}")


# The class of my quiz
class QuizInterface:
    def __init__(self):
        # creates a tkinter window
        self.root = Tk()
        # Gives the window a title of "Quiz"
        self.root.title("Quiz")
        # Gives the window the dimensions of 1280x720 pixels
        self.root.geometry("1280x720")

        # Creates a canvas that covers the entire tkitner window
        # This allows me to create shapes on the tkinter window
        # It's a dark blue colour so this essentially sets the background colour of the window
        canvas = Canvas(self.root, width=1280, height=720, bg="#063385")
        canvas.pack()

        # Creates a light blue rectangle for the "Quiz" text to go into at the top of the window
        canvas.create_rectangle(0, 0, 1282, 90, fill="#83CBEB")

        # Places the text "Quiz" in the rectangle created for it
        Title = Label(self.root, text="Quiz", bg="#83CBEB", fg="#000000", font=("System", 55))
        Title.place(relx=0.5, y=0, anchor="n")  # Center horizontally using relx and set y at 0

        # Creates a rectangle for everything but the buttons to go into
        canvas.create_rectangle(19, 122, 1258, 389, fill="#83CBEB")

        # Defines a list of dictionaries as questions
        self.questions = [
            {"question": "What's the space complexity of a bubble sort?", "answer": "O(1)", "options": ["O(1)", "O(n)", "O(n^2)", "O(nlogn)"]},
            {"question": "What's the space complexity of an insertion sort?", "answer": "O(1)", "options": ["O(1)", "O(n)", "O(n^2)", "O(nlogn)"]},
            {"question": "What's the space complexity of a merge sort?", "answer": "O(n)", "options": ["O(1)", "O(n)", "O(n^2)", "O(nlogn)"]},
            {"question": "What's the space complexity of a quick sort?", "answer": "O(n)", "options": ["O(1)", "O(n)", "O(n^2)", "O(nlogn)"]},
            {"question": "What's the time complexity of a bubble sort?", "answer": "O(n^2)", "options": ["O(1)", "O(n)", "O(n^2)", "O(nlogn)"]},
            {"question": "What's the time complexity of an insertion sort?", "answer": "O(n^2)", "options": ["O(1)", "O(n)", "O(n^2)", "O(nlogn)"]},
            {"question": "What's the time complexity of a merge sort?", "answer": "O(nlogn)", "options": ["O(1)", "O(n)", "O(n^2)", "O(nlogn)"]},
            {"question": "What's the time complexity of a quick sort?", "answer": "O(nlogn)", "options": ["O(1)", "O(n)", "O(n^2)", "O(nlogn)"]},
            {"question": "For sorting a large dataset, which algorithm would generally sort faster: Bubble Sort or Quick Sort?", "answer": "Quick Sort", "options": ["Bubble Sort", "Quick Sort"]},
            {"question": "For sorting a large dataset, which algorithm would generally sort faster: Insertion Sort or Merge Sort?", "answer": "Merge Sort", "options": ["Insertion Sort", "Merge Sort"]},
            {"question": "For sorting a small dataset, which algorithm would generally sort faster: Bubble Sort or Merge Sort?", "answer": "Bubble Sort", "options": ["Bubble Sort", "Merge Sort"]},
            {"question": "For sorting a small dataset, which algorithm would generally sort faster: Insertion Sort or Quick Sort?", "answer": "Insertion Sort", "options": ["Insertion Sort", "Quick Sort"]},
            {"question": "Which algorithm would generally sort faster: Quick Sort or Merge Sort?", "answer": "Quick Sort", "options": ["Quick Sort", "Merge Sort"]},
            {"question": "Which algorithm would generally sort faster: Bubble Sort or Insertion Sort?", "answer": "Insertion Sort", "options": ["Bubble Sort", "Insertion Sort"]}
        ]

        #puts the list "self.questions" into a random order each time the quiz is played
        random.shuffle(self.questions)

         # The number of questions the user has answered starts from 0 (variable)
        self.current_question = 0
        # The user's score starts from 0 (variable)
        self.score = 0
        # The timer for the quiz starts at 2 minutes (120 seconds) (variable)
        self.time_remaining = 120  

        # This is a label that will be repetitively configured to display the current question to be answered
        self.question_label = Label(self.root, text="", wraplength=400, font=("system", 20), bg="#83CBEB", fg="#000000")
        self.question_label.place(relx=0.5, y=140, anchor="n")  # Placed under the rectangle

        # This is a label that will be repetitively configured to display the timer
        self.timer_label = Label(self.root, text="02:00", font=("system", 20), fg="#000000", bg="#83CBEB")
        self.timer_label.place(x=30, y=140) 

        # This is a label that will be repeatedly configured to display the user's current score
        self.score_label = Label(self.root, text="Score: 0", font=("system", 20), fg="#000000", bg="#83CBEB")
        self.score_label.place(x=30, y=170)  # Placed near the top-left corner

        # This is a label to display the number of remaining questions
        self.questions_remaining_label = Label(self.root, text="Questions remaining: 13", font=("system", 20), fg="#000000", bg="#83CBEB")
        self.questions_remaining_label.place(x=30, y=200)  # Positioned under the score label

        # Creates the 4 multiple choice answer buttons 
        self.option_buttons = [Button(self.root, text="", font=("Arial", 12), wraplength=400, bg="#f0f0f0", fg="#000000", activebackground="#63A6D1", relief="solid") for _ in range(4)]

        # Displays the first question and multiple choice answer buttons on the screen and other elements
        self.load_question()

        # Creates a variable that will flag when the timer should end
        self.end_timer = False
        
        # Starts the timer
        self.update_timer()

        

        # Updates the GUI every time an event occurs
        self.root.mainloop()

    # Carries out processes when a user answers a question
    def select_answer(self, selected_option):
        correct_answer = self.questions[self.current_question]["answer"]

        # If the user answered correctly, increment their score by 1
        if selected_option.strip() == correct_answer.strip():
            self.score += 1

        # Makes the buttons unclickable after answering a question (for a short while)
        for button in self.option_buttons:
            button.config(state="disabled")

        # Load the next question after the answer is displayed (without delay)
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.end_quiz()  # End the quiz if there are no more questions
            
    def load_question(self):
        # Ensure quiz ends if there are no remaining questions
        if self.current_question >= len(self.questions):
            return

        # calculates how many questions there are left to be answered and stores it 
        remaining_questions = len(self.questions) - self.current_question - 1  

        # Updates the "Questions remaining" label to display the current number of questions left for the user to answer
        self.questions_remaining_label.config(text=f"Questions remaining: {remaining_questions}")

        # Retrieves the current dictionary for the current question to be answered
        question_data = self.questions[self.current_question]

        # Displays the current question to be answered on the user's screen
        self.question_label.config(text=question_data["question"])

        options = question_data["options"]  # Gets the multiple choice answers for the current question
        num_buttons = len(options)

        # Defines the positions of the buttons 
        positions = [
            (16, 420),  # Top-left button
            (648, 420),  # Top-right button
            (16, 580),  # Bottom-left button
            (648, 580)   # Bottom-right button
        ]

        # Update the buttons based on the number of options
        for i in range(4):

            #creates the multiple choice buttons and displays them on the screen
            if i < num_buttons:
                self.option_buttons[i].config(
                    text=options[i],
                    command=lambda opt=options[i]: self.select_answer(opt),
                    bg="#0a57db", 
                    fg="white",  
                    activebackground="#083da5",  
                    activeforeground="white",  
                    bd=0, 
                    highlightthickness=0,  
                    font=("System", 50),  
                    wraplength=400  
                )
                self.option_buttons[i].place(x=positions[i][0], y=positions[i][1], width=616, height=120)
            #This makes sure no more buttons that are needed are created
            else:
                # Hide the extra buttons
                self.option_buttons[i].place_forget()

       

        # Updates score label
        self.score_label.config(text=f"Score: {self.score}")

        # Makes buttons clickable again
        for button in self.option_buttons:
            button.config(state="normal")

    # Updates the timer every second
    def update_timer(self):
        # Stops the timer if the quiz has ended
        if self.end_timer:  # If the quiz is finished, stop updating the timer
            return
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.config(text=f"{minutes:02}:{seconds:02}")

        # If the timer is greater than 0 minutes and 0 seconds, decrement the timer by 1 second
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.root.after(1000, self.update_timer)  # Continue updating the timer every second
        else:  # When the timer reaches 0, end the quiz
            self.end_quiz()
            

    # Ends the quiz when it is called
    def end_quiz(self):
        # hides the label from the screen when the quiz ends.
        self.score_label.config(text="")
        # Sets the flag to stop the timer
        self.end_timer = True
        #Stores how long the user took to complete the quiz
        self.time_taken = 120 - self.time_remaining
        # Subtracts 1 from the variable to make the values in the database more accurate.
        self.time_taken = self.time_taken-1
        # makes the questions_remaining_label disappear from the screen
        self.questions_remaining_label.config(text=" ")
        # Displays the user's final score
        self.question_label.config(text=f"Your final score is: {self.score}/{len(self.questions)}")        
        # Hides all the buttons from the user's screen
        for btn in self.option_buttons:
            btn.destroy()
        #wait for 5 seconds and then remove the quiz screen from the user's screen
        self.root.after(5000, self.root.destroy)
        #Inserts the user's quiz results into the "Quiz" table
        self.insert_quiz_result(self.time_taken,self.score)


    #Inserts the user's end of quiz results into the "Quiz" table once the quiz has ended     
    def insert_quiz_result(self, time_taken, score):
        
        
        # Connects to the database
        conn = sqlite3.connect('Sortshowcase.db')
        cursor = conn.cursor()

        # Insert result into the Quiz table
        cursor.execute("""
        INSERT INTO Quiz (username, score, time_taken)
        VALUES (?, ?, ?)
        """, (username, score, time_taken))

        # Commit the transaction
        conn.commit()

        # Close the connection
        conn.close()
       











    

#The class of the navigation bar
class NavigationBar:
    def __init__(self, parent, on_logout=None, on_home=None, on_sorts=None,on_quiz=None):

        self.on_logout = on_logout  
        self.on_home = on_home      
        self.on_sorts = on_sorts
        self.on_quiz=on_quiz

        # Background color of the navigation bar
        self.nav_bg_color = '#83CBEB'

        # creates and displays the frame of the navigation bar
        self.navbar_frame = Frame(parent, bg=self.nav_bg_color, width=1280, height=90)
        self.navbar_frame.pack(fill=X)

        # adds the header titled "Sort showcase" to the navigation bar's frame.
        self.header_label = Label(self.navbar_frame, text="Sort Showcase", bg=self.nav_bg_color,fg='Black', font=("System", 24, "bold"), padx=20)
        self.header_label.pack(side=LEFT, padx=20)

        # Adds a black bar to visually seperate the "Sort showcase" header from the menubars/buttons
        self.separator = Frame(self.navbar_frame, bg='black', width=2, height=60)
        self.separator.pack(side=LEFT, padx=(10, 20), pady=15)

        # Call the method that creates the buttons/menubas present in the navigation bar
        self.create_buttons()

    # This is the method that creates the buttons/menubas present in the navigation bar
    def create_buttons(self):
        # When the user hovers over the a button it changes to white
        def on_enter(event):
            event.widget.config(bg='white', fg='black')
        # When the user no longer hovers over the button it stops being white
        def on_leave(event):
            event.widget.config(bg=self.nav_bg_color, fg='Black')

        # Creates all the buttons/menubars present in the navigation  bar
        self.home_button = Button(self.navbar_frame, text="Home", bg=self.nav_bg_color,fg='Black', bd=0, padx=30, pady=20, font=("System", 22))
        self.sorts_button = Button(self.navbar_frame, text="Sorts", bg=self.nav_bg_color,fg='Black', bd=0, padx=30, pady=20, font=("System", 22))
        self.quiz_button = Button(self.navbar_frame, text="Quiz", bg=self.nav_bg_color,fg='Black', bd=0, padx=30, pady=20, font=("System", 22))
        self.logout_button = Button(self.navbar_frame, text="Log out", bg=self.nav_bg_color,fg='Black', bd=0, padx=30, pady=20, font=("System", 22))

        #Displays all the buttons/menubars in the navigation bar
        for button in [self.home_button, self.sorts_button, self.quiz_button, self.logout_button]:
            button.pack(side=LEFT, padx=30)
            #binds the buttons to the on_enter and on_leave methods
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

        #links the buttons to their respective methods/actions
        self.home_button.config(command=self.on_home)
        self.sorts_button.config(command=self.on_sorts)
        self.quiz_button.config(command=self.on_quiz)
        self.logout_button.config(command=self.on_logout)




class App:
    def __init__(self):
        # Creates a tkinter window
        root = Tk()
        self.root = root
        # Gives the window the title of "sort showcase"
        self.root.title("Sort Showcase")
        #Gives the window a size of 1280x720 pixels
        self.root.geometry("1280x720")
        #gives the window a dark blue background colour
        self.root.configure(bg='#063385')
        #Displays the navigation bar (on all necessary screens)
        self.nav_bar = NavigationBar(self.root, on_logout=self.log_out,on_home=self.show_home_screen, on_sorts=self.show_sorts_screen, on_quiz=self.show_quiz_screen)
        # This creates the space where content from each screen will be displayed on whilst that screen is toggled
        self.main_frame = Frame(self.root, bg='#063385')
        self.main_frame.pack(fill=BOTH, expand=True)

         #Creates the Frame in which the sorting animations will be displayed in
        self.sorts_frame = Frame(self.root, width=688, height=550, bg='#063385')  
        self.sorts_frame.place(x=19, y=163)  
        self.sorts_frame.pack_propagate(False) 
        #updates the gui everytime an event occurs
        #displays the home screen when the app is initalised
        self.show_home_screen()
        self.root.mainloop()
    #Displays the home screen
    def show_home_screen(self):
        self.sorts_frame.destroy()
        #destroys everything but the screen itself and the navgation bar
        for widget in self.main_frame.winfo_children():
            widget.destroy()
         # Displays a welcome message, welcoming the user by their username
        label = Label(self.main_frame, text=f"Welcome {username}!",bg='#063385', fg='white', font=("System", 24))
        label.pack(pady=20)
        
        #connects to the database
        conn = sqlite3.connect('SortShowcase.db')
        cursor = conn.cursor()
        #Fetches  the user's quiz results from the database
        cursor.execute('''
    SELECT MAX(score), AVG(score), AVG(time_taken)
    FROM Quiz
    WHERE username = ?;
''', (username,))
        #This is the quiz results stored as an array
        result = cursor.fetchone()
        #These values store 0 if the user has not played a quiz before
        #stores the high score
        high_score = result[0] if result[0] is not None else 0
        #stores the average score
        avg_score = result[1] if result[1] is not None else 0
        #stores the average time
        avg_time = result[2] if result[2] is not None else 0

        # Display the high score, average score, and average time
        stats_label = Label(self.main_frame, text=f"High Score: {high_score}\nAverage Score: {avg_score:.2f}\nAverage Time: {avg_time:.2f} seconds", 
                               bg='#063385', fg='white', font=("System", 20))
        stats_label.pack(pady=20)
        #closes the connection to the database
        conn.close()

    # Stops any animations from the sort screen appearing on the home screen 
        for widget in self.sorts_frame.winfo_children():
            widget.destroy()
            
    #displays the sort screen
    def show_sorts_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
         # Create the control frame for slider and buttons
        self.control_frame = Frame(self.main_frame, bg="#063385", pady=10)
        self.control_frame.pack()

        # Displays the data set size that the slider toggles
        self.slider_label = Label(self.control_frame, text="Select Number of Integers (N):", bg="#063385", fg="white")
        self.slider_label.pack(side=LEFT, padx=10)
        
        # Creates the slider and gives it an asthetic look to match the screens and displays it.
        self.n_slider = Scale(
            self.control_frame,
            from_=5,
            to=100,
            orient='horizontal',
            bg="#063385",
            fg="white",
            troughcolor="#83CBEB",
            highlightthickness=0
        )
        self.n_slider.set(20)
        self.n_slider.pack(side=LEFT,padx=10)
        #Creates the button with the text "Start Animation".
        self.start_button = Button(self.control_frame, text="Start Animation", command=self.create_animations, bg="#83CBEB")
        self.start_button.pack(side=LEFT, padx=( 10))  # Adjusted the right padding

         
        #Creates the square with the Big 0 notation of the Bubble sort
        Bubble_square = Canvas(self.main_frame, width=260, height=270, bg='#0a57db' , bd=0, highlightthickness=0)
        Bubble_square.place(x=716, y=63)
        Bubble_square.create_text(130, 30, text="Bubble Sort", fill="white", font=("System", 18, "bold"))
        Bubble_square.create_line(0, 45, 260, 45, fill="white", width=2)
        Bubble_square.create_text(130, 75, text="Big O Notation:", fill="white", font=("System", 14, "italic"))
        Bubble_square.create_text(130, 105, text="• O(n^2) - time complexity", fill="white", font=("System", 12))
        Bubble_square.create_text(130, 135, text="• O(1) - space complexity", fill="white", font=("System", 12))
       #Creates the square with the Big 0 notation of the Insetion sort
        Insertion_square = Canvas(self.main_frame, width=260, height=270, bg='#0a57db' , bd=0, highlightthickness=0)
        Insertion_square.place(x=1016, y=63)
        Insertion_square.create_text(130, 30, text="Insertion Sort", fill="white", font=("System", 18, "bold"))
        Insertion_square.create_line(0, 45, 260, 45, fill="white", width=2)
        Insertion_square.create_text(130, 75, text="Big O Notation:", fill="white", font=("System", 14, "italic"))
        Insertion_square.create_text(130, 105, text="• O(n^2) - time complexity", fill="white", font=("System", 12))
        Insertion_square.create_text(130, 135, text="• O(1) - space complexity", fill="white", font=("System", 12))
        #Creates the square with the Big 0 notation of the Merge sort
        Merge_square = Canvas(self.main_frame, width=260, height=270, bg='#0a57db' , bd=0, highlightthickness=0)
        Merge_square.place(x=716, y=343)
        Merge_square.create_text(130, 30, text="Merge Sort", fill="white", font=("System", 18, "bold"))
        Merge_square.create_line(0, 45, 260, 45, fill="white", width=2)
        Merge_square.create_text(130, 75, text="Big O Notation:", fill="white", font=("System", 14, "italic"))
        Merge_square.create_text(130, 105, text="• O(nlogn) - time complexity", fill="white", font=("System", 12))
        Merge_square.create_text(130, 135, text="• O(n) - space complexity", fill="white", font=("System", 12))
        #Creates the square with the Big 0 notation of the Quick sort
        Quick_square = Canvas(self.main_frame, width=260, height=270, bg='#0a57db' , bd=0, highlightthickness=0)
        Quick_square.place(x=1016, y=343)
        Quick_square.create_text(130, 30, text="Quick Sort", fill="white", font=("System", 18, "bold"))
        Quick_square.create_line(0, 45, 260, 45, fill="white", width=2)
        Quick_square.create_text(130, 75, text="Big O Notation:", fill="white", font=("System", 14, "italic"))
        Quick_square.create_text(130, 105, text="• O(nlogn) - time complexity", fill="white", font=("System", 12))
        Quick_square.create_text(130, 135, text="• O(n) - space complexity", fill="white", font=("System", 12))

        #Creates the Frame in which the sorting animations will be displayed in
        self.sorts_frame = Frame(self.root, width=688, height=550, bg='#063385')  
        self.sorts_frame.place(x=19, y=163)  
        self.sorts_frame.pack_propagate(False)  


        

    #displays the quiz screen       
    def show_quiz_screen(self):
         QuizInterface()
    #log's the user out
    def log_out(self):
        #closes the tkinter window with the navigation bar on it
        self.root.destroy()
        #creates an instance of the "LoginGui" class
        LoginGui()

    # Function to create and display the sorting animations
    def create_animations(self):
        # clears any animations that are already on the screen 
        for widget in self.sorts_frame.winfo_children():
            widget.destroy()

        # Gets the size of the dataset from the slider
        N = self.n_slider.get()
        # Creates an unsorted data set
        A = [x + 1 for x in range(N)]
        random.shuffle(A)

        # Creates the figure and sets the background colour
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        # Determines the space between the animations
        plt.subplots_adjust(wspace=0.4, hspace=0.4)
        axs = axs.flatten()

        # Set figure background color to dark blue
        fig.patch.set_facecolor('#063385')

        # Changes the colours present in all of the animations
        for ax in axs:
            ax.set_facecolor('#063385')  
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.tick_params(axis='both', colors='white')  

        # Creates the animation for the bubble sort
        axs[0].set_title("Bubble Sort", color='white')
        bar_rects1 = axs[0].bar(range(len(A)), A, align="edge", color='#83CBEB')
        axs[0].set_xlim(0, N)
        axs[0].set_ylim(0, int(1.07 * N))
        text1 = axs[0].text(0.02, 0.95, "", transform=axs[0].transAxes, color='white')
        iteration1 = [0]
        anim1 = animation.FuncAnimation(fig, func=update_fig, fargs=(bar_rects1, iteration1, text1),
                                        frames=bubblesort(A.copy()), interval=1, repeat=False)

        # Creates the animation for the insertion sort
        axs[1].set_title("Insertion Sort", color='white')
        bar_rects2 = axs[1].bar(range(len(A)), A, align="edge", color='#83CBEB')
        axs[1].set_xlim(0, N)
        axs[1].set_ylim(0, int(1.07 * N))
        text2 = axs[1].text(0.02, 0.95, "", transform=axs[1].transAxes, color='white')
        iteration2 = [0]
        anim2 = animation.FuncAnimation(fig, func=update_fig, fargs=(bar_rects2, iteration2, text2),
                                        frames=insertionsort(A.copy()), interval=1, repeat=False)

        # Creates the animation for the merge sort
        axs[2].set_title("Merge Sort", color='white')
        bar_rects3 = axs[2].bar(range(len(A)), A, align="edge", color='#83CBEB')
        axs[2].set_xlim(0, N)
        axs[2].set_ylim(0, int(1.07 * N))
        text3 = axs[2].text(0.02, 0.95, "", transform=axs[2].transAxes, color='white')
        iteration3 = [0]
        anim3 = animation.FuncAnimation(fig, func=update_fig, fargs=(bar_rects3, iteration3, text3),
                                        frames=mergesort(A.copy()), interval=1, repeat=False)

        # Creates the animation for the quick sort
        axs[3].set_title("Quick Sort", color='white')
        bar_rects4 = axs[3].bar(range(len(A)), A, align="edge", color='#83CBEB')
        axs[3].set_xlim(0, N)
        axs[3].set_ylim(0, int(1.07 * N))
        text4 = axs[3].text(0.02, 0.95, "", transform=axs[3].transAxes, color='white')
        iteration4 = [0]
        anim4 = animation.FuncAnimation(fig, func=update_fig, fargs=(bar_rects4, iteration4, text4),
                                        frames=quicksort(A.copy(), 0, len(A) - 1), interval=1, repeat=False)

        # Displays the animations in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.sorts_frame)
        canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        canvas.draw()

class LoginGui:

    def __init__(self):
        #loads login screen when class is initialised
        self.create_login_window()

    def create_login_window(self):
        # Initializes the login window
        self.login_window = Tk()
        self.login_window.geometry("1280x720")
        #Sets the title of the actual window as "Login"
        self.login_window.title('Login')

        #Stores image of background picture in python program
        filename = PhotoImage(file='Background.png')
        #Places background picture on tkinter window effectively setting it as the background image
        background_label = Label(self.login_window, image=filename)
        background_label.place(relwidth=1, relheight=1)

        #Displays the title "sort showcase" onto the screen
        title = Label(self.login_window, text="Sort showcase", bg="#063385", fg="#83cbeb", font=("Courier New", 50))
        title.pack(pady=100)

        #Displays the title "Login" onto the screen
        login_title = Label(self.login_window, text="Login", bg="#063385", fg="#c1e5f5", font=("Courier New", 35))
        login_title.place(x=580, y=187)

        #Creates the "username" text box and it's corresponding text input box
        Label(self.login_window, text="username", bg="#00b0f0", fg="white",font=("Courier New", 45), borderwidth=3, relief="solid").place(x=378, y=250)
        self.username_entry = Entry(self.login_window, width=7, font=("Courier New", 47), borderwidth=3, relief="solid")
        self.username_entry.place(x=690, y=250)

        #Creates the "password" text box and it's corresponding text input box
        Label(self.login_window, text="Password", bg="#00b0f0", fg="white",font=("Courier New", 45), borderwidth=3, relief="solid").place(x=378, y=350)
        self.password_entry = Entry(self.login_window, width=7, font=("Courier New", 47), show='*', borderwidth=3, relief="solid")
        self.password_entry.place(x=690, y=350)

        #Creates the login button and displays it onto the users screen
        login_button = Button(self.login_window, text='Login', bg="#156082", width=82, height=3, fg="white", borderwidth=3, relief="solid", command=self.login)
        login_button.place(x=378, y=450)

        #Creates the sign up button and displays it onto the users screen
        signup_button = Button(self.login_window, text='Sign Up', bg="#0b3041", width=41, height=3, fg="white", borderwidth=3, relief="solid", command=self.create_account_window)
        signup_button.place(x=520, y=520)
        #updates the GUI everytime an event occurs
        self.login_window.mainloop()

    def login(self):
        #connects to the datbase
        conn = sqlite3.connect('SortShowcase.db')
        cursor = conn.cursor()
        #makes username into a global variable
        global username
        # Stores what is in the username text box
        username = self.username_entry.get()
        # stores what is in the password text box and hashes it.
        password = hashlib.sha256(self.password_entry.get().encode()).hexdigest()
        # Fetches the account from the database that matches credentials given.
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?;', (username, password))
        # Stores the fetched account (if it exists in the database)
        user = cursor.fetchone()
         # If a user's credentials are valid log them in
        if user:
            messagebox.showinfo("Login Success", "Login successful!")
            # Makes the login window disappear from the users screen
            self.login_window.destroy()
            #create an instance of the "App" class
            App()
        # If a user's credentials aren't valid do not log them in.            
        else:
            messagebox.showerror("Login failed", "Invalid credentials")
        #closes the database
        conn.close()

    def MainMenuWindow(self, user):
        # Close the login window and open the profile window
        self.login_window.destroy()
        self.profile_window = Tk()
        self.profile_window.title(f'Profile of {user[0]}')
        Label(self.profile_window, text=f'Name: {user[0]}').pack()
        self.profile_window.mainloop()

    def create_account_window(self):
        #Destroys the login screen
        self.login_window.destroy()
        #Initializes the sign-up window
        self.signup_window = Tk()
        self.signup_window.geometry("1280x720")
        #Sets the title of the actual window as "Sign up"
        self.signup_window.title('Sign Up')

        #Stores image of the background picture in the python program
        filename = PhotoImage(file='Background.png')
        #Places background picture on tkinter window effectively setting it as the background image
        background_label = Label(self.signup_window, image=filename)
        background_label.place(relwidth=1, relheight=1)

        #Displays the title "sort showcase" onto the screen
        title = Label(self.signup_window, text="Sort showcase", bg="#063385", fg="#83cbeb", font=("Courier New", 50))
        title.pack(pady=100)

        #Displays the title "Signup" onto the screen
        signup_title = Label(self.signup_window, text="Sign Up", bg="#063385", fg="#c1e5f5", font=("Courier New", 35))
        signup_title.place(x=580, y=187)

        #Creates the "username" text box and it's corresponding text input box
        Label(self.signup_window, text="username", bg="#00b0f0", fg="white", font=("Courier New", 45), borderwidth=3, relief="solid").place(x=378, y=250)
        self.username_entry = Entry(self.signup_window, width=7, font=("Courier New", 47), borderwidth=3, relief="solid")
        self.username_entry.place(x=690, y=250)

        #Creates the "username" text box and it's corresponding text input box
        Label(self.signup_window, text="Password", bg="#00b0f0", fg="white", font=("Courier New", 45), borderwidth=3, relief="solid").place(x=378, y=350)
        self.password_entry = Entry(self.signup_window, width=7, font=("Courier New", 47), show='*', borderwidth=3, relief="solid")
        self.password_entry.place(x=690, y=350)

        #Creates the sign up button and displays it onto the users screen
        signup_button = Button(self.signup_window, text='Sign Up', bg="#0b3041", width=82, height=3, fg="white", borderwidth=3, relief="solid", command=self.create_account)
        signup_button.place(x=378, y=450)

        #Creates the "Login" button that directs the user back to the login screen when pressed and displays it
        back_to_login_button = Button(self.signup_window, text='Login', bg="#156082", width=41, height=3, fg="white", borderwidth=3, relief="solid", command=self.back_to_login)
        back_to_login_button.place(x=520, y=520)
        #updates the GUI everytime an event occurs
        self.signup_window.mainloop()

    def back_to_login(self):
        # Close the sign-up window and return to the login window
        self.signup_window.destroy()
        self.create_login_window()

    def create_account(self):
        # Connect to the database to create a new account
        conn = sqlite3.connect('SortShowcase.db')
        cursor = conn.cursor()
        #stores what is stored in the username text input box
        username = self.username_entry.get()
        #stores what is in the password text input box
        password = self.password_entry.get()

        # Check if username or password is empty
        if not username or not password:
            #Displays a error message box on the screen
            messagebox.showerror("Sign Up Failed", "Both username and password are required.")
            conn.close()
            #The user will not have an account created
            return
        #hashes the user's inputted password
        password = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        #checks if the user's username already exists in the database
        if cursor.fetchone():
            #if it does then an account will not be created and a error message box is displayed
            messagebox.showerror("Sign Up Failed", "Username already exists")
        else:
            #if it doesnt then an account will be created
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            #commits the transaction to the database
            conn.commit()
            #displays a posootive message box
            messagebox.showinfo("Account Created", "Account successfully created!")
            #loads the login screen
            self.back_to_login()
        #closes the database
        conn.close()

# Run the application
login_gui = LoginGui()
