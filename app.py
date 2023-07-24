{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import gradio as gr\n",
    "\n",
    "def greet(Person):\n",
    "    \n",
    "    return \"Hello \" + Person + \"!\"\n",
    "\n",
    "demo = gr.Interface(fn=greet, inputs=\"text\", outputs=\"text\")\n",
    "\n",
    "demo.launch()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "demo = gr.Interface(\n",
    "    fn=greet,\n",
    "    inputs=gr.Textbox(lines=2, placeholder=\"Name Here...\"),\n",
    "    outputs=\"text\",\n",
    ")\n",
    "demo.launch()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import gradio as gr\n",
    "\n",
    "with gr.Blocks() as demo:\n",
    "    name = gr.Textbox(label=\"Name\")\n",
    "    output = gr.Textbox(label=\"Output Box\")\n",
    "    greet_btn = gr.Button(\"Greet\")\n",
    "    greet_btn.click(fn=greet, inputs=name, outputs=output, api_name=\"greet\")\n",
    "   \n",
    "\n",
    "demo.launch()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from transformers import pipeline\n",
    "import gradio as gr\n",
    "\n",
    "pipe = pipeline(\"translation\", model=\"Helsinki-NLP/opus-mt-en-es\")\n",
    "\n",
    "demo = gr.Interface.from_pipeline(pipe)\n",
    "demo.launch()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.0"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
