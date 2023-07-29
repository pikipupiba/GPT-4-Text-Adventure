import gradio as gr
from session import *

def build_gm_message(engine, scenario, npc, environment, rules):
    return f"System:\r\n{engine}\r\n\r\nScenario:\r\n{scenario}\r\n\r\nNPC:\r\n{npc}\r\n\r\nEnvironment:\r\n{environment}\r\n\r\nRules:\r\n{rules}"

with gr.Blocks() as game_master_area:
    with gr.Row():
        file_name = gr.Textbox(lines=1, label="File Name", interactive=True, scale=10, value="default")
        save = gr.Button(value="Save", scale=1)
        load = gr.Button(value="Load", scale=1)

    engine = gr.Textbox(lines=10, label="Engine", interactive=True)
    scenario = gr.Textbox(lines=10, label="Scenario", interactive=True)
    npc = gr.Textbox(lines=10, label="NPC", interactive=True)
    environment = gr.Textbox(lines=10, label="Environment", interactive=True)
    rules = gr.Textbox(lines=10, label="Rules", interactive=True)
    gm_message = gr.Textbox(lines=50, label="GM Message", interactive=False)

    engine.change(fn=build_gm_message, inputs=[engine, scenario, npc, environment, rules], outputs=[gm_message])
    scenario.change(fn=build_gm_message, inputs=[engine, scenario, npc, environment, rules], outputs=[gm_message])
    npc.change(fn=build_gm_message, inputs=[engine, scenario, npc, environment, rules], outputs=[gm_message])
    environment.change(fn=build_gm_message, inputs=[engine, scenario, npc, environment, rules], outputs=[gm_message])
    rules.change(fn=build_gm_message, inputs=[engine, scenario, npc, environment, rules], outputs=[gm_message])

    save.click(fn=save_session, inputs=[file_name, engine, scenario, npc, environment, rules], outputs=[])
    load.click(fn=load_session, inputs=[file_name], outputs=[file_name, engine, scenario, npc, environment, rules])