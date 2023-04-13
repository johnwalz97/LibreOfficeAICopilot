# WIP: LibreOffice AI Copilot

This is a project I started to learn how to use the OpenAI APIs and specifically the gpt-3.5-turbo chat API. The goal is to add very basic AI
functionality to LibreOffice Writer. I welcome any contributions to this project.

LibreOffice AI Copilot is a plugin for LibreOffice that integrates OpenAI's GPT-3.5 Turbo model to provide AI-assisted writing features. This plugin enables users to generate context-aware text completions and suggestions directly within their LibreOffice documents, helping them improve their writing speed and quality.

## Features

- In-place prompt: Select a portion of text in your document and the AI will generate a context-aware completion based on the selected text.
- Completion: Place the cursor at a specific location in your document and the AI will generate a completion based on the text before the cursor.

## Installation

1. Ensure you have LibreOffice installed on your system.
2. Download the `libreoffice-ai-copilot.oxt` file from the repository.
3. Open LibreOffice and navigate to the Extension Manager by clicking `Tools > Extension Manager`.
4. Click `Add` and select the `libreoffice-ai-copilot.oxt` file to install the plugin.
5. Restart LibreOffice after the installation is complete.

## Usage

- To use the in-place prompt feature, select a portion of text in your document, then click `AI Copilot > In-place Prompt` or use the assigned keyboard shortcut (CMD+Shift+X on Mac, CTRL+Shift+X on Windows).
- To use the completion feature, place the cursor at the desired location in your document, then click `AI Copilot > Completion` or use the assigned keyboard shortcut (CMD+Shift+D on Mac, CTRL+Shift+D on Windows).

## API Key Configuration

To use this plugin, you need to have an API key from OpenAI. To set up the API key:

1. Open the `libre_copilot/copilot.py` file in a text editor.
2. Locate the following line:

```python
openai.api_key = "YOUR_API_KEY_HERE"
```

3. Replace `YOUR_API_KEY_HERE` with your OpenAI API key and save the changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit pull requests for any improvements or bug fixes. If you have any questions or feature requests, feel free to open an issue.
