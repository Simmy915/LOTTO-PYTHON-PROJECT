import datetime
import socket
from tkinter import *
from tkinter import messagebox
import re
import rsaidnumber
from dateutil import relativedelta
import random
import uuid
import requests
import tkinter.ttk as ttk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from playsound import playsound


class LottoFunction:
    def __init__(self):
        self.counter = 0

    def compare(self, list1, list2):
        try:
            self.counter = 0
            if len(list1) != len(list2):
                raise IndexError
            else:
                for i in range(len(list1)):
                    if list1[i] == list2[i]:
                        self.counter += 1

            return self.counter

        except IndexError:
            print("The length of the lists must be equal")

#THIS IS THE ERROR MESSAGE FOR THE EMAIL, FIRST NAME AND EMPTY ERROE

class EmailError(Exception):
    pass


class IdLengthError(Exception):
    pass


class FirstNameError(Exception):
    pass


class EmptyError(Exception):
    pass


class LottoGUI(LottoFunction):
    def __init__(self, master):
        ##THIS IS THE WINDOW SET-UP OF THE LOGIN PAGE AND WHAT THE USER WILL SEE !!!!!!!
        super().__init__()
        self.master = master
        self.master.title("Login Page: Simphiwe Sithole")
        self.master.geometry("500x400")
        self.master.config(bg="green")


        self.name = ""
        self.email = ""
        self.address = ""
        self.set_count = 0
        self.play_win = None
        self.claim_win = None
        self.total_win = 0
        self.win_nums = []
        self.game_no = 0
        self.results = []
        self.img2 = PhotoImage(file='images/ithuba.png')  # lotto ball image
        self.img2 = self.img2.subsample(16)

        #THIS IS THE LOGIN PAGE OR FRAME
        self.frame = Frame(self.master, width=450, height=220, bg="green")
        self.frame.place(x=25, y=95)

        ##THIS IS THE LOGIN PAGE THAT THE USER WILL SEE WHEN THEY LOGIN
        self.lbl_subhead = Label(self.frame, text="PLEASE FILL IN YOUR DETAILS", font="Arial 12 bold", bg="green",
                                 fg="red")
        self.lbl_subhead.place(x=150, y=12)
        img = PhotoImage(file='images/ithuba.png')
        img = img.subsample(4)
        lbl_image = Label(self.master, image=img, bg="green")
        lbl_image.place(x=130, y=5)

        ##THESE ARE THE PLAYERS DETAILS THAT THEY WILL NEED TO FILL IN, IN ORDER TO PROCEED
        self.lbl_name = Label(self.frame, text="Your Name", font="Garuda 12", bg="orange", fg="white")
        self.lbl_email = Label(self.frame, text="Your Email Address", font="Garuda 12", bg="blue", fg="white")
        self.lbl_id = Label(self.frame, text="Your RSA ID number", font="Garuda 12", bg="red", fg="white")
        self.lbl_address = Label(self.frame, text="Your Address", font="Garuda 12", bg="purple", fg="white")
        self.lbl_name.place(x=40, y=60)
        self.lbl_email.place(x=40, y=100)
        self.lbl_id.place(x=40, y=140)
        self.lbl_address.place(x=40, y=180)

        ##THESE ARE THE WIDGETS THAT WILL BE USED TO LOGIN BY THE USER !!!!!!
        self.entry_email = Entry(self.frame, borderwidth="0")
        self.entry_name = Entry(self.frame, borderwidth="0")
        self.entry_id = Entry(self.frame, borderwidth="0")
        self.entry_address = Entry(self.frame, borderwidth="0")
        self.entry_name.place(x=245, y=60)
        self.entry_email.place(x=245, y=100)
        self.entry_id.place(x=245, y=140)
        self.entry_address.place(x=245, y=180)

        ##THIS IS THE BUTTON THAT WILL BE USED BY THE USER TO VALIDATE WHETHER THE DETAILS THAT THEY HAVE
        self.btn_validate = Button(self.master, text="Validate", bg="green", fg="red", borderwidth="0",
                                   highlightbackground="blue", activebackground="yellow",
                                   activeforeground="white", command=self.validate)
        self.btn_validate.place(x=25, y=330)

        #THIS IS THE BUTTON THAT WILL CLEAR WHAT IS IN THE BOX, WHEN ACTIVATED !!!!!
        self.btn_clear = Button(self.master, text="Clear", bg="green", fg="red", borderwidth="0",
                                highlightbackground="yellow", activebackground="blue", activeforeground="white",
                                command=self.clear)
        self.btn_clear.place(x=350, y=330)

        ##THIS IS THE BUTTON THAT WILL QUIT THE APP WHEN ACTIVATED BY THE USER!
        self.btn_exit = Button(self.master, text="Exit", bg="green", fg="red", borderwidth="0",
                               highlightbackground="yellow", activebackground="red",
                               activeforeground="blue", command=exit)
        self.btn_exit.place(x=425, y=330)

        self.master.mainloop()

#THIS THE ENTRY FIELDS FUCTIONS THAT WILL CLEAR LOG ENTRY FIELDS !!!
    def clear(self):
        self.entry_name.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_id.delete(0, 'end')

    # THIS IS DATA TRAPPING !!!
    def validate(self):
        try:

            if self.entry_email.get() == "" or self.entry_id == "" or self.entry_name == "":
                raise EmptyError

            #THIS WILL VALIDATE THE EMAIL ADDRESS PROVIDED AND ID
            regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
            if not (re.search(regex, self.entry_email.get())):
                raise EmailError

            int(self.entry_id.get())
            _id = (self.entry_id.get())
            date_of_birth = rsaidnumber.parse(_id).date_of_birth
            if len(_id) < 13 or len(_id) > 13:
                raise IdLengthError


            elif relativedelta.relativedelta(datetime.datetime.today(), date_of_birth).years < 18:
                playsound("sounds/You win sound effect 5.mp3")
                messagebox.showerror("Oops!", "You are too young to play!")

            else:
                self.name = self.entry_name.get()
                self.email = self.entry_email.get()
                self.address = self.entry_address.get()
                messagebox.showinfo("Hello there!", "Let us play!")
                playsound("sounds/You win sound effect 5.mp3")
                root.withdraw()
                self.play_window(self.play_win)

        except EmptyError:
            messagebox.showerror(message="All fields need to be  filled")

        except EmailError:
            messagebox.showerror("Oops!", "That email is invalid")

        except DNS.Base.TimeoutError:
            messagebox.showerror("Oops!", "Have a look at your connection.")

        except ValueError:
            messagebox.showerror("Oops!", "RSA ID number invalid")

        except IdLengthError:
            messagebox.showerror("Oops!", "RSA ID number must have 13 digits only")

    def play_window(self, window):
        #THIS IS THE WINDOW SET UP
        self.master.withdraw()
        window = Toplevel()
        result_text = ""
        window.title("rt PlayScreen")
        window.geometry("930x350")
        window.config(bg="green")

        def submit():

            try:
                results = [int(spin1.get()), int(spin2.get()), int(spin3.get()), int(spin4.get()),
                           int(spin5.get()), int(spin6.get())]
                for num in results:
                    if num > 49 or num <= 0:
                        raise ValueError

                self.results.append(results)
                m = messagebox.askyesno(message="Wanna make another ticket submission?")
                if m:
                    reset()

                else:
                    print_result(result_text)
                    btn_submit.config(state='disabled')
                    btn_play_again.config(state='normal')
                    btn_claim.config(state='normal')

            except ValueError:
                messagebox.showerror(message="The range for the number selection is 0 - 49")

        def reset():
            spin1.delete(0, "end")
            spin2.delete(0, "end")
            spin3.delete(0, "end")
            spin4.delete(0, "end")
            spin5.delete(0, "end")
            spin6.delete(0, "end")

            spin1.insert(0, 1)
            spin2.insert(0, 1)
            spin3.insert(0, 1)
            spin4.insert(0, 1)
            spin5.insert(0, 1)
            spin6.insert(0, 1)

        def play_again():

            reset()
            self.win_nums.clear()
            for i in range(6):
                rand_num = random.randint(1, 49)
                while rand_num in self.win_nums:
                    rand_num = random.randint(1, 49)
                self.win_nums.append(rand_num)
            print(self.win_nums)
            btn_submit.config(state="normal")
            btn_play_again.config(state='disabled')
            btn_claim.config(state='disabled')

        def print_result(result_txt_var):
            win_nums_text = "Winning combination: {}, {}   {}, {}, {}, {}".format(self.win_nums[0], self.win_nums[1], self.win_nums[2], self.win_nums[3], self.win_nums[4], self.win_nums[5],)
            lbl_win_nums.config(text=win_nums_text)
            self.game_no += 1
            result_txt_var += "Game {}\n".format(self.game_no)

            winnings = {0: 0, 1: 0, 2: 20, 3: 100.50, 4: 2384, 5: 8584, 6: 10000000}
            self.set_count += len(self.results)
            count = 0
            for i in range(len(self.results)):

                print(self.results)
                print(self.win_nums)
                count = self.compare(self.results[i], self.win_nums)
                result_txt_var += "Set {}\n" \
                                  "Number of winning numbers: {}\n" \
                                  "Winnings: R{}\n\n".format(i + 1, count, winnings[count])
                self.total_win = self.total_win + winnings[count]


            if winnings[count] == 0:
                playsound("sounds/You win sound effect 5.mp3")
            else:
                playsound("sounds/You win sound effect 5.mp3")


            text.config(state='normal')
            text.insert(END, result_txt_var)
            text.config(state='disabled')

        def claim():
            if len(self.results) == 0:
                pass
            else:
                day = datetime.datetime.today().day
                month = datetime.datetime.today().month
                year = datetime.datetime.today().year
                with open('testing.txt', 'a') as f:
                    f.write('Date: {}/{}/{}\n'.format(day, month, year))
                    f.write("Name: {}\n".format(self.name))
                    f.write("   Address: {}\n".format(self.address))
                    f.write("   PlayerID: {}\n".format(player_id))
                    f.write("   Email: {}\n".format(self.email))
                    f.write("   Winning combination: {}\n".format(self.win_nums))
                    f.write("   Total sets played for all games: {}\n".format(self.set_count))
                    f.write("   Total winnings due: R{}\n\n".format(self.total_win))

        lbl_head = Label(window, text="GO ON! TAKE A CHANCE!", width=10, font="Arial 12 bold", bg="green",
                         fg="red")
        lbl_head.place(x=150, y=10)

        lbl_image2 = Label(window, image=self.img2, bg="green")
        lbl_image2.place(x=240, y=1)


        player_id = str(uuid.uuid1())
        player_id = player_id[0:5]
        player_id_text = "Player ID: {}".format(player_id)
        lbl_player = Label(window, text=player_id_text, bg="green", fg="red", font="Arial 12")
        lbl_player.place(x=180, y=100)


        lbl_select = Label(window, text="Make your selection:", font="Arial 11 bold", bg="green",
                           fg="red")
        lbl_select.place(x=150, y=200)


        spin1 = Spinbox(window, from_=1, to=49, width=5)
        spin2 = Spinbox(window, from_=1, to=49, width=5)
        spin3 = Spinbox(window, from_=1, to=49, width=5)
        spin4 = Spinbox(window, from_=1, to=49, width=5)
        spin5 = Spinbox(window, from_=1, to=49, width=5)
        spin6 = Spinbox(window, from_=1, to=49, width=5)
        spin1.place(x=45, y=255)
        spin2.place(x=115, y=255)
        spin3.place(x=185, y=255)
        spin4.place(x=255, y=255)
        spin5.place(x=325, y=255)
        spin6.place(x=405, y=255)


        btn_submit = Button(window, text="Submit", bg="green", fg="red", borderwidth="0",
                            highlightbackground="white", activebackground="white", activeforeground="yellow",
                            command=submit)
        btn_submit.place(x=215, y=300)


        for x in range(6):
            rand_num = random.randint(1, 49)
            while rand_num in self.win_nums:
                rand_num = random.randint(1, 49)
            self.win_nums.append(rand_num)
        print(self.win_nums)

        lbl_win_nums = Label(window, text="Winning numbers: ",bg="purple", fg="white", font="Arial 12")
        lbl_win_nums.place(x=510, y=40)


        head_result = Label(window, text="Did you win?", font="Arial 11 bold", bg="red", fg="white")
        head_result.place(x=620, y=10)
        frame = Frame(window, height=50)
        frame.place(x=510, y=70)
        text = Text(frame)
        text.config(height=12.4, width=40)
        text.config(state='disabled')
        scroll = Scrollbar(frame)
        text.config(yscrollcommand=scroll.set)
        scroll.config(command=text.yview)
        scroll.pack(side=RIGHT, fill=Y)
        text.pack(fill=Y)


        btn_play_again = Button(window, text="Try Again", bg="green", fg="white", borderwidth="0",
                                highlightbackground="red", activebackground="yellow",
                                activeforeground="blue", state='disabled', command=lambda: [self.results.clear(),
                                                                                               play_again()])
        btn_play_again.place(x=510, y=300)


        btn_claim = Button(window, text="Claim", bg="green", fg="white", borderwidth="0",
                           highlightbackground="blue", activebackground="red",
                           activeforeground="yellow", state='disabled', command=lambda: [claim(), self.claim_window(self.claim_win),
                                                                        window.destroy()])
        btn_claim.place(x=620, y=300)
        btn_exit = Button(window, text="Exit", bg="green", fg="white", borderwidth="0",
                          highlightbackground="white", activebackground="white",
                          activeforeground="red", command=exit)
        btn_exit.place(x=834, y=300)

    @staticmethod
    def claim_window(window):
        window = Toplevel()
        window.title("Claim your prize")
        window.geometry("485x350")
        window.config(bg="green")

        def convert_currency():
            try:

                if entry_currency.get() == "":
                    raise EmptyError

                cur_api = requests.get("https://v6.exchangerate-api.com/v6/b8b53279722ad58c70d2a2de/latest/ZAR")
                cur_data = cur_api.json()


                amount = prize * cur_data["conversion_rates"][entry_currency.get().upper()]


                amount_text = '{} ({})'.format(round(amount, 2), entry_currency.get().upper())
                entry_winning_amount.config(state='normal')
                entry_winning_amount.delete("1.0", "end")
                entry_winning_amount.insert(END, amount_text)
                entry_winning_amount.tag_configure('center', justify=RIGHT)
                entry_winning_amount.tag_add('center', 1.0, 'end')
                entry_winning_amount.config(state='disabled')

            except EmptyError:
                messagebox.showerror(message="Currency is required")

            except KeyError:
                messagebox.showerror("Oops!", "Please make sure you entered the correct currency")

            except requests.exceptions.ConnectionError:
                messagebox.showerror(message="Check internet connection")

        def email():
            try:

                with open('testing.txt', 'r') as file:
                    for _line in file:
                        if "Name" in _line:
                            name = _line[6:-1]
                        if "Email" in _line:
                            email_id = _line[10:-1]
                        if "ID" in _line:
                            player_id = _line[13:-1]


                numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
                for num in numbers:
                    if str(num) in entry_account_holder_name.get():
                        raise NameError


                int(entry_account_num.get())

                if entry_account_holder_name.get() == "":
                    raise EmptyError

                if entry_account_num.get() == "":
                    raise EmptyError

                if selection_bank.get() == "Please make your selection!":
                    raise EmptyError


                sender_email_id = 'rtplaylotto@gmail.com'
                receiver_email_id = email_id
                password = "SFUqK9E3mvkcrR7"
                subject = "Well done!"
                msg = MIMEMultipart()
                msg['From'] = sender_email_id
                msg['To'] = ", ".join(receiver_email_id)
                msg['Subject'] = subject
                body = "Congratulations {} on winning {}\n" \
                       "Please find details below\n\n" \
                       "Bank: {}\n" \
                       "Account holder: {}\n" \
                       "Account number: {}\n" \
                       "Player ID: {}\n\n" \
                       "YOur winnings should reflect. please check your account statement.\n\n" \
                       "Best regards\n" \
                       "rtplay Team".format(name, entry_winning_amount.get(1.0, END), selection_bank.get(),
                                            entry_account_holder_name.get(), entry_account_num.get(), player_id)
                msg.attach(MIMEText(body, 'plain'))
                text = msg.as_string()
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(sender_email_id, password)
                s.sendmail(sender_email_id, receiver_email_id, text)
                s.quit()

                #THIS IS THE END
                messagebox.showinfo("THIS IS THE END!", "Please check your mailbox")
                window.destroy()
                root.destroy()

            except NameError:
                messagebox.showerror(message="Please make sure account holder is correct")

            except EmptyError:
                messagebox.showerror(message="Please make sure your bank details are correct")

            except ValueError:
                messagebox.showerror(message="Please make sure your account numbers is in digits")

            except socket.gaierror:
                messagebox.showerror(message="PLease check if you are still connected")


        lbl_head = Label(window, text="Your bank details are required!", font="Arial 12 bold", bg="green", fg="red")
        lbl_head.place(x=125, y=10)


        lbl_account_holder = Label(window, text="Please enter the account holder name", font="Ariel 12", bg="green", fg="red")
        entry_account_holder_name = Entry(window, width=16)
        lbl_account_holder.place(x=20, y=80)
        entry_account_holder_name.place(x=300, y=85)


        lbl_account_num = Label(window, text="Please enter your bank account number", font="Ariel 12", bg="green", fg="red")
        entry_account_num = Entry(window, width=16)
        lbl_account_num.place(x=20, y=110)
        entry_account_num.place(x=300, y=115)

        #THIS IS THE CURRENCY CONVERTER FOR THE PLAYER
        lbl_currency = Label(window, text="Enter currency code", font="Ariel 12", bg="green", fg="red")
        entry_currency = Entry(window, width=16)
        btn_currency = Button(window, text="convert currency", font="Arial 11", pady=0, padx=13, width=52, bg="green",
                              fg="red", borderwidth="0", highlightbackground="blue", activebackground="yellow",
                              activeforeground="blue", command=convert_currency)
        btn_currency.place(x=20, y=190)
        lbl_currency.place(x=20, y=160)
        entry_currency.place(x=300, y=163)


        with open("testing.txt", "r") as f:
            for line in f:
                if "winnings" in line:
                    prize = round(float(line[24:-1]), 2)


        lbl_winning_amount_head = Label(window, text="Total winnings", font="Arial 12", bg="green", fg="red")
        entry_winning_amount = Text(window, borderwidth="0", bg="blue", height=1, width=18)
        entry_winning_amount.insert(END, "{} (ZAR)".format(prize))
        entry_winning_amount.tag_configure('center', justify=RIGHT)
        entry_winning_amount.tag_add('center', 1.0, 'end')
        lbl_winning_amount_head.place(x=20, y=240)
        entry_winning_amount.place(x=300, y=247)

        #THESE ARE THE BANK SELECTION WIDGETS
        lbl_bank = Label(window, text="Choose your bank", font="Arial 12", bg="green", fg="blue")
        selection_bank = StringVar()
        options_banks = ['Capitec', 'AfricanBank', 'ABSA', 'Standard Bank']
        option_menu_banks = ttk.OptionMenu(window, selection_bank, "please make your choice", *options_banks)
        lbl_bank.place(x=20, y=50)
        option_menu_banks.place(x=300, y=50)


        btn_confirm = Button(window, text='Confirm', font="Arial 11", pady=0, padx=12, width=44, bg="green", fg="red",
                             borderwidth="0", highlightbackground="blue", activebackground="yellow",
                             activeforeground="green", command=email)
        btn_confirm.place(x=20, y=280)



if __name__ == '__main__':
    root = Tk()
    LottoGUI(root)
