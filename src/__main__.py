from Tkinter import *
from tkFont import Font
import getpass
import aerochat.database

class Application(Frame):
    def __init__(self, mdb, master=None):
        Frame.__init__(self, master)
        self.mdb = mdb
        messages = mdb.get_latest_messages(0, 10)
        self.last_timestamp = 0 if len(messages) == 0 else messages[-1].timestamp
        self.message_poller = aerochat.database.MessagePoller(mdb, self.last_timestamp, self.poller_callback)
        self.pack()

        self.frame_bottom = Frame(self)
        self.frame_bottom.pack(side=BOTTOM)

        self.text_draft = Text(self.frame_bottom)
        self.text_draft.insert(END, "")
        self.text_draft["background"] = "#F5F5F5"
        self.text_draft["height"] = 4
        self.text_draft["width"] = 26
        self.text_draft["wrap"] = WORD
        self.text_draft.focus_force()
        self.text_draft.bind("<KeyRelease>", self.key_release_callback)
        self.text_draft.pack(side=LEFT)

        self.button_send = Button(self.frame_bottom, command=self.submit_draft)
        self.button_send["text"] = "Send"
        self.button_send["height"] = 1
        self.button_send.pack(side=RIGHT)

        self.scrollbar_received = Scrollbar(self)
        self.scrollbar_received.pack(side=RIGHT, fill=Y)

        self.font_bold = Font(weight="bold")
        self.text_received = Text(self)
        self.text_received.tag_config("bold", font=self.font_bold)
        self.add_first_messages_to_text_received(messages)
        self.text_received["background"] = "#E4EEF3"
        self.text_received["height"] = 25
        self.text_received["width"] = 50
        self.text_received["wrap"] = WORD
        self.text_received.config(state=DISABLED)
        self.text_received.config(yscrollcommand=self.scrollbar_received.set)
        self.scrollbar_received.config(command=self.text_received.yview)
        self.text_received.pack(side=BOTTOM)

        self.message_poller.start()

    def poller_callback(self, messages):
        self.text_received.config(state=NORMAL)
        self.add_messages_to_text_received(messages)
        self.text_received.config(state=DISABLED)

    def add_messages_to_text_received(self, messages):
        for m in messages:
            self.text_received.insert(END, m.sender, "bold")
            self.text_received.insert(END, ": ")
            self.text_received.insert(END, m.text)
            self.text_received.insert(END, "\n")

        self.text_received.yview(END)

    def add_first_messages_to_text_received(self, messages):
        if len(messages) > 0:
            self.text_received.insert(END, "--- Old Messages ---\n", "bold")
            self.add_messages_to_text_received(messages)
            self.text_received.insert(END, "--- New Messages ---\n", "bold")

    def key_release_callback(self, event):
        if event.keysym == 'Return':
            self.submit_draft()

    def submit_draft(self):
        text = self.text_draft.get(1.0, END).strip()
        self.text_draft.delete(1.0, END)
        self.mdb.publish_message(text)

    def destroy(self):
        self.message_poller.stop()
        Frame.destroy(self)

def main():
    mdb = aerochat.database.MessageDatabase(getpass.getuser(), "./messages")
    root = Tk()
    root.minsize(250, 400)
    root.maxsize(250, 400)
    app = Application(mdb, master=root)
    app.master.title("AeroChat")
    root.mainloop()

if __name__ == '__main__':
    main()