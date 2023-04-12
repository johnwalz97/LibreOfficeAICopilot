import sys

import uno
import unohelper
from com.sun.star.document import XEventListener
from com.sun.star.task import XJobExecutor

# TODO: fix this hack to get the openai package to load
sys.path.append(
    "/Users/jwalz/Library/Caches/pypoetry/virtualenvs/libreoffice-copilot--obLNlTe-py3.10/lib/python3.10/site-packages"
)
import openai

# TODO: add mechanism to get the API key from the user
with open("/Users/jwalz/Code/Personal/libreoffice-copilot/openai_api_key.txt", "r") as f:
    contents = f.read().strip()
    # find line that starts with OPENAI_API_KEY and get the value after the =
    openai.api_key = contents.split("=")[1].strip()


class AICopilot(unohelper.Base, XJobExecutor, XEventListener):
    def __init__(self, context):
        """
        Initialize the AI Copilot class.

        Args:
            context: The component context.
        """
        self.context = context
        self.desktop = self.createUnoService("com.sun.star.frame.Desktop")
        self.dispatchhelper = self.createUnoService("com.sun.star.frame.DispatchHelper")

    def trigger(self, command):
        """
        Called when the service is called from a menu or keyboard shortcut.

        Args:
            command (str): The command that was called.
        """
        if command == "inplacePrompt":
            try:
                response = self.inplace_prompt_api(self.get_selected_text())
            except Exception as e:
                self.show_message_box("OpenAI API Error:\n", str(e))
                return

            self.replace_selected_text(response.choices[0].message.content.strip())

        elif command == "completion":
            try:
                response = self.completion_api(self.get_text_with_cursor())
            except Exception as e:
                self.show_message_box("OpenAI API Error:\n", str(e))
                return

            self.insert_text(response.choices[0].message.content.strip())

    def get_text_with_cursor(self):
        """
        Get the text of the document with a placeholder for the cursor position.

        Returns:
            str: The text of the document with the cursor position marked.
        """
        model = self.desktop.getCurrentComponent()
        if not hasattr(model, "CurrentController"):
            return ""
        view_cursor = model.CurrentController.getViewCursor()
        
        # Create text cursor for the entire document
        text_cursor = model.Text.createTextCursorByRange(view_cursor)
        
        # Get all text before the cursor
        text_cursor.gotoRange(view_cursor, False)
        text_cursor.gotoStart(True)
        text_before_cursor = text_cursor.getString()
        
        # Get all text after the cursor
        text_cursor.gotoRange(view_cursor, False)
        text_cursor.gotoEnd(True)
        text_after_cursor = text_cursor.getString()

        return text_before_cursor + "[CURSOR_LOCATION]" + text_after_cursor

    def insert_text(self, text):
        """
        Insert the given text at the current cursor position in the document.

        Args:
            text (str): The text to insert.
        """
        model = self.desktop.getCurrentComponent()
        if not hasattr(model, "CurrentController"):
            return
        cursor = model.CurrentController.getViewCursor()
        cursor.Text.insertString(cursor, text, False)

    def get_selected_text(self):
        """
        Get the selected text in the document.

        Returns:
            str: The selected text or an empty string if no text is selected.
        """
        model = self.desktop.getCurrentComponent()
        if not hasattr(model, "CurrentController"):
            return ""
        selection = model.CurrentController.getSelection()
        if not selection.hasElements():
            return ""
        return selection.getByIndex(0).getString()

    def replace_selected_text(self, new_text):
        """
        Replace the selected text with the provided text.

        Args:
            new_text (str): The text to replace the selected text with.
        """
        model = self.desktop.getCurrentComponent()
        if not hasattr(model, "CurrentController"):
            return
        selection = model.CurrentController.getSelection()
        if not selection.hasElements():
            return
        selected_range = selection.getByIndex(0)
        selected_range.setString(new_text)

    def inplace_prompt_api(self, text):
        """
        Call the OpenAI API with the given text.

        Args:
            text (str): The text to send to the OpenAI API.

        Returns:
            dict: The response from the OpenAI API.
        """
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
        )

    def completion_api(self, text):
        """
        Call the OpenAI API with the given text and return the completion.

        Args:
            text (str): The text to send to the OpenAI API.

        Returns:
            dict: The response from the OpenAI API.
        """
        prompt = u"""Complete the following PROMPT_TEXT with your best guess as to what comes after the [CURSOR_LOCATION].
Imagine that you are a human writing a document.
You will match the style, formatting and tone of the PROMPT_TEXT.
You will not change the PROMPT_TEXT but add your own text to it at the location designated by [CURSOR_LOCATION].
You will respond with just the text to be inserted at the [CURSOR_LOCATION].
You will try to make your response as long as possible.


Example:
PROMPT_TEXT=```There are a lot of ways that AI can improve your life. While some of them are still in the early stages of development, [CURSOR_LOCATION]```
RESPONSE=```there are many that you can use today.

One great way to start incorporating AI into your life is to use it to help you with your meal-planning. You can use AI to help you plan your meals, and even to help you find recipes that you might not have thought of before. Some of the most powerful AI models today can even understand the ingredients that you have on hand and create recipes from scratch based on them.```

Example:
PROMPT_TEXT=```I just returned from a three month sabbatical spent mostly offline diving through history and I feel like I’ve returned to an alien planet full of serious utopian and dystopian thinking swirling simultaneously. I find myself nodding along because both the best case and worst case scenarios could happen. But also cringing because the passion behind these declarations has no room for nuance. Everything feels extreme and fully of binaries. I am truly astonished by the the deeply entrenched deterministic thinking that feels pervasive in these conversations.

[CURSOR_LOCATION]

What is deterministic thinking?
Simply put, determinism is “if x, then y.” It is the notion that if we do something (x), a particular outcome (y) is inevitable. Determinisms are not inherently positive or negative. It is just as deterministic to say “if we build social media, the world will be a more connected place” as it is to say “social media will destroy democracy.”```
RESPONSE=```Deterministic thinking is a blinkering force, the very opposite of rationality even though many people who espouse deterministic thinking believe themselves to be hyper rational. Deterministic thinking tends to seed polarization and distrust as people become entrenched in their vision of the future. Returning to the modern world, I’m finding myself frantically waving my hands in a desperate attempt to get those around me to take a deep breath (or maybe 100 of them). Given that few people can see my hand movements from my home office, I’m going to pretend like it’s 2004 and blog my thoughts in the hopes that this post might calm at least one person down. Or, maybe, if I’m lucky, it’ll be fed into an AI model and add a tiny bit of nuance.```


PROMPT_TEXT=```PROMPT_TEXT_HERE```""".replace("PROMPT_TEXT_HERE", text)

        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )

    def show_message_box(self, title, message):
        """
        Show a message box with the specified title and message.

        Args:
            title (str): The title of the message box.
            message (str): The content of the message box.
        """
        frame = self.desktop.ActiveFrame
        window = frame.ContainerWindow
        window.Toolkit.createMessageBox(
            window,
            uno.Enum("com.sun.star.awt.MessageBoxType", "INFOBOX"),
            uno.getConstantByName("com.sun.star.awt.MessageBoxButtons.BUTTONS_OK"),
            title,
            message,
        ).execute()

    # boilerplate code below this point
    def createUnoService(self, name):
        """
        Create an instance of the specified UNO service.

        Args:
            name (str): The name of the service to create.

        Returns:
            object: The created UNO service.
        """
        return self.context.ServiceManager.createInstanceWithContext(name, self.context)

    def disposing(self, _):
        """
        Empty disposing method for the XEventListener interface.

        Args:
            _ (object): The source object of the event.
        """
        pass

    def notifyEvent(self, _):
        """
        Empty notifyEvent method for the XEventListener interface.

        Args:
            _ (object): The event object.
        """
        pass


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    AICopilot,
    "org.libreoffice.jwalz.AICopilot",
    ("com.sun.star.task.JobExecutor",),
)
