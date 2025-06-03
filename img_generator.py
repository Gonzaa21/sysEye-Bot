import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
import io

# indentify last snapshot
SNAPSHOT_DIR = "C:\\Users\\Usuario\\Downloads\\sysEye\\snapshots"
def load_last_snapshot(snapshot_dir=SNAPSHOT_DIR):
    with open(os.path.join(snapshot_dir, "latest.txt"), "r") as f:
        filename = f.read().strip()
    filepath = os.path.join(snapshot_dir, filename)
    return pd.read_csv(filepath), filename

# save png in memory temporarily
buf = io.BytesIO()

# generate graphs for each component
def generate_graphs(df: pd.DataFrame):
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(3, 2, figure=fig)
    texts = []

    # System Information
    if "Operating System" in df.columns:
        try:
            os_info = json.loads(df["Operating System"].iloc[0].replace("'", "\""))
            texts.append(f"Operative System: {os_info}")
        except Exception:
            texts.append(f"Operative System: {df['Operating System'].iloc[0]}")

    if "OS Version" in df.columns:
        try:
            version = float(df["OS Version"].iloc[0])
            texts.append(f"Version: {version}")
        except:
            texts.append(f"Version: {df['OS Version'].iloc[0]}")

    # RAM Memory
    if all(col in df.columns for col in ["Used RAM", "Free RAM", "Available RAM"]):
        try:
            used = float(df["Used RAM"].iloc[0])
            free = float(df["Free RAM"].iloc[0])
            available = float(df["Available RAM"].iloc[0])
            ax_ram = fig.add_subplot(gs[0, 0])
            ax_ram.pie([used, free, available],
                       labels=["Used", "Free", "Available"],
                       autopct="%1.1f%%", startangle=90)
            ax_ram.set_title("RAM Memory")
        except ValueError:
            pass

    # SWAP Memory
    if all(col in df.columns for col in ["Total SWAP", "Used SWAP", "Free SWAP"]):
        try:
            used_swap = float(df["Used SWAP"].iloc[0])
            free_swap = float(df["Free SWAP"].iloc[0])
            ax_swap = fig.add_subplot(gs[0, 1])
            ax_swap.pie([used_swap, free_swap],
                        labels=["Used", "Free"],
                        autopct="%1.1f%%", startangle=90)
            ax_swap.set_title("SWAP Memory")
        except ValueError:
            pass

    # CPU
    if "Global CPU Usage" in df.columns:
        try:
            cpu_usage = float(df["Global CPU Usage"].iloc[0])
            ax_cpu = fig.add_subplot(gs[1, 0])
            ax_cpu.bar(["Use CPU"], [cpu_usage], color="orange")
            ax_cpu.set_ylim(0, 100)
            ax_cpu.set_title("Global use CPU (%)")
        except ValueError:
            pass
        
    if "Number of CPUs" in df.columns:
        try:
            cpus = df["Number of CPUs"].iloc[0]
            texts.append(f"CPU Cores: {cpus}")
        except:
            texts.append("CPU Cores: Unknown")


    # Processes
    if "Number of Processes" in df.columns:
        try:
            process = df["Number of Processes"].iloc[0]
            texts.append(f"Processes: {process}")
        except:
            texts.append("Processes in execution: Unknown")
            
    # Disk
    if all(col in df.columns for col in ["Disk Total Space", "Disk Available Space"]):
        try:
            total_disk = float(df["Disk Total Space"].iloc[0])
            available_disk = float(df["Disk Available Space"].iloc[0])
            ax_disk = fig.add_subplot(gs[1, 1])
            ax_disk.bar(["Total", "Available"], [total_disk, available_disk], color=["blue", "green"])
            ax_disk.set_title("Disk Space")
        except ValueError as e:
            print(f'{e}')
    
    
    # Network
    if all(col in df.columns for col in ["Net Name", "Net Down", "Net Up"]):
        try:
            name = df["Net Name"].iloc[0]
            down_network = float(df["Net Down"].iloc[0])
            up_network = float(df["Net Up"].iloc[0])

            ax_network = fig.add_subplot(gs[2, 0])

            # bars
            ax_network.bar(name, down_network, label="Download", color="red")
            ax_network.bar(name, up_network, bottom=down_network, label="Upload", color="green")
            
            # labels
            ax_network.set_title("Network Usage")
            ax_network.set_ylabel("Bytes")
            ax_network.legend(loc="upper right")

            # labels on bars
            ax_network.text(x=name, y=down_network/2, s=f"{int(down_network)}", ha='center', va='center', color='white')
            ax_network.text(x=name, y=down_network + up_network/2, s=f"{int(up_network)}", ha='center', va='center', color='white')

        except ValueError as e:
            print(f'{e}')
    
    # texts
    if texts:
        full_text = "\n".join(texts)
        fig.text(0.01, 1, full_text, fontsize=10, va="top", ha="left")
        
    # Ajust layout and save to buffer
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    
    buf.seek(0)