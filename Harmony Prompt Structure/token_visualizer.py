#!/usr/bin/env python3
"""
Harmony Token Detail Viewer - Enhanced Edition
Advanced visualization of how text becomes tokens in Harmony format
"""

import sys
import argparse
from typing import List, Dict, Tuple, Optional
from openai_harmony import (
    load_harmony_encoding,
    HarmonyEncodingName,
    Role,
    Message,
    Conversation,
    SystemContent,
    DeveloperContent,
)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.columns import Columns
from rich.progress import track
from rich.rule import Rule
from rich.layout import Layout
from rich.syntax import Syntax
from rich.tree import Tree

console = Console()

class TokenVisualizer:
    """Enhanced token visualization with multiple display modes"""
    
    # Comprehensive token mappings
    SPECIAL_TOKENS = {
        200006: ("<|start|>", "Message boundary start", "🚪"),
        200007: ("<|end|>", "Message boundary end", "🔚"),
        200008: ("<|message|>", "Content separator", "📝"),
        200009: ("<|channel|>", "Channel marker", "📡"),
        200010: ("<|return|>", "Response complete", "↩️"),
        200011: ("<|call|>", "Tool call", "🔧"),
        200012: ("<|constrain|>", "Type constraint", "📏"),
    }
    
    ROLE_TOKENS = {
        1428: ("user", "User speaking", "👤"),
        173781: ("assistant", "Assistant speaking", "🤖"),
        16811: ("system", "System configuration", "⚙️"),
        58517: ("developer", "Developer instructions", "💻"),
    }
    
    CHANNEL_TOKENS = {
        10750: ("final", "User-facing response", "💬"),
        11746: ("analysis", "Chain of thought", "🧠"),
        25112: ("commentary", "Tool/preamble", "🔍"),
    }
    
    def __init__(self):
        self.enc = load_harmony_encoding(HarmonyEncodingName.HARMONY_GPT_OSS)
        
    def decode_token(self, token: int) -> Tuple[str, str, str]:
        """Decode a single token and return (decoded, type, emoji)"""
        if token in self.SPECIAL_TOKENS:
            decoded, desc, emoji = self.SPECIAL_TOKENS[token]
            return decoded, "SPECIAL", emoji
        elif token in self.ROLE_TOKENS:
            decoded, desc, emoji = self.ROLE_TOKENS[token]
            return decoded, "ROLE", emoji
        elif token in self.CHANNEL_TOKENS:
            decoded, desc, emoji = self.CHANNEL_TOKENS[token]
            return decoded, "CHANNEL", emoji
        else:
            # Text token
            try:
                decoded = self.enc.decode_utf8([token])
                if not decoded or decoded.isspace():
                    if token == 0:
                        return "!", "TEXT", "📄"
                    else:
                        return "[space]", "TEXT", "📄"
                return decoded, "TEXT", "📄"
            except:
                return f"[{token}]", "UNKNOWN", "❓"
    
    def create_token_tree(self, tokens: List[int]) -> Tree:
        """Create a tree visualization of token structure"""
        tree = Tree("🌳 [bold]Token Structure[/bold]")
        
        current_message = None
        current_section = None
        
        for i, token in enumerate(tokens):
            decoded, token_type, emoji = self.decode_token(token)
            
            if decoded == "<|start|>":
                current_message = tree.add(f"{emoji} Message {i//5 + 1}")
                current_section = None
            elif decoded in ["user", "assistant", "system", "developer"]:
                if current_message:
                    current_section = current_message.add(f"{emoji} Role: {decoded}")
            elif decoded == "<|message|>":
                if current_message:
                    current_section = current_message.add(f"{emoji} Content")
            elif token_type == "TEXT" and current_section:
                current_section.add(f"{emoji} '{decoded}' [{token}]")
            elif current_message and token_type == "SPECIAL":
                current_message.add(f"{emoji} {decoded}")
        
        return tree
    
    def create_flow_diagram(self, tokens: List[int]) -> Panel:
        """Create a flow diagram of the token sequence"""
        flow = Text()
        
        for i, token in enumerate(tokens):
            decoded, token_type, emoji = self.decode_token(token)
            
            if i > 0:
                flow.append(" → ", style="dim")
            
            if token_type == "SPECIAL":
                flow.append(f"{emoji}{decoded}", style="bold red")
            elif token_type == "ROLE":
                flow.append(f"{emoji}{decoded}", style="bold yellow")
            elif token_type == "CHANNEL":
                flow.append(f"{emoji}{decoded}", style="bold magenta")
            elif token_type == "TEXT":
                # Combine consecutive text tokens
                if i == 0 or self.decode_token(tokens[i-1])[1] != "TEXT":
                    # Start of text sequence
                    text_tokens = []
                    j = i
                    while j < len(tokens) and self.decode_token(tokens[j])[1] == "TEXT":
                        text_tokens.append(tokens[j])
                        j += 1
                    combined = self.enc.decode_utf8(text_tokens)
                    flow.append(f"📄'{combined}'", style="bold green")
                    # Skip the tokens we just processed
                    for _ in range(len(text_tokens) - 1):
                        if i + 1 < len(tokens):
                            i += 1
        
        return Panel(flow, title="🔄 Token Flow", border_style="blue")
    
    def create_detailed_table(self, tokens: List[int]) -> Table:
        """Create a detailed breakdown table"""
        table = Table(title="🔬 Detailed Token Analysis", box=box.DOUBLE_EDGE, show_lines=True)
        table.add_column("#", style="dim", width=4, justify="right")
        table.add_column("Token ID", style="yellow", width=10, justify="right")
        table.add_column("Hex", style="cyan", width=10)
        table.add_column("Type", style="magenta", width=12)
        table.add_column("Decoded", style="green", width=20)
        table.add_column("Description", style="white", width=30)
        table.add_column("Icon", width=4, justify="center")
        
        # First pass: identify text token sequences
        text_sequences = []
        i = 0
        while i < len(tokens):
            decoded, token_type, _ = self.decode_token(tokens[i])
            if token_type == "TEXT":
                start = i
                text_tokens = []
                while i < len(tokens):
                    d, t, _ = self.decode_token(tokens[i])
                    if t == "TEXT":
                        text_tokens.append(tokens[i])
                        i += 1
                    else:
                        break
                # Decode the complete text sequence
                combined = self.enc.decode_utf8(text_tokens)
                text_sequences.append((start, text_tokens, combined))
            else:
                i += 1
        
        # Second pass: create table rows
        for i, token in enumerate(tokens):
            decoded, token_type, emoji = self.decode_token(token)
            hex_value = f"0x{token:X}"
            
            # Check if this token is part of a text sequence
            in_sequence = None
            for start, text_tokens, combined in text_sequences:
                if start <= i < start + len(text_tokens):
                    in_sequence = (start, text_tokens, combined)
                    break
            
            # Get description
            if token in self.SPECIAL_TOKENS:
                description = self.SPECIAL_TOKENS[token][1]
            elif token in self.ROLE_TOKENS:
                description = self.ROLE_TOKENS[token][1]
            elif token in self.CHANNEL_TOKENS:
                description = self.CHANNEL_TOKENS[token][1]
            elif token_type == "TEXT" and in_sequence:
                start, text_tokens, combined = in_sequence
                if i == start:
                    # First token in sequence - show combined result
                    description = f"Text: '{combined}' ({len(text_tokens)} tokens)"
                else:
                    # Continuation token
                    description = f"└─ part of '{combined}'"
            else:
                description = "Unknown token"
            
            # Format decoded value for display
            if len(decoded) > 20:
                decoded_display = decoded[:17] + "..."
            else:
                decoded_display = decoded
            
            table.add_row(
                str(i),
                str(token),
                hex_value,
                token_type,
                decoded_display,
                description,
                emoji
            )
        
        return table
    
    def create_statistics_panel(self, tokens: List[int], message: str) -> Panel:
        """Create comprehensive statistics"""
        stats = Table(show_header=False, box=box.SIMPLE)
        stats.add_column("Category", style="cyan", width=20)
        stats.add_column("Value", style="yellow")
        
        # Count token types
        special_count = sum(1 for t in tokens if t in self.SPECIAL_TOKENS)
        role_count = sum(1 for t in tokens if t in self.ROLE_TOKENS)
        channel_count = sum(1 for t in tokens if t in self.CHANNEL_TOKENS)
        text_count = len(tokens) - special_count - role_count - channel_count
        
        # Calculate statistics
        stats.add_row("Total Tokens", str(len(tokens)))
        stats.add_row("Special Tokens", f"{special_count} ({special_count/len(tokens)*100:.1f}%)")
        stats.add_row("Role Tokens", f"{role_count} ({role_count/len(tokens)*100:.1f}%)")
        stats.add_row("Channel Tokens", f"{channel_count} ({channel_count/len(tokens)*100:.1f}%)")
        stats.add_row("Text Tokens", f"{text_count} ({text_count/len(tokens)*100:.1f}%)")
        stats.add_row("", "")  # Separator
        stats.add_row("Message Length", f"{len(message)} chars")
        stats.add_row("Unique Tokens", str(len(set(tokens))))
        stats.add_row("Compression Ratio", f"{len(message)/len(tokens):.2f} chars/token")
        stats.add_row("Bytes per Token", f"{len(message.encode('utf-8'))/len(tokens):.2f}")
        
        return Panel(stats, title="📊 Statistics", border_style="green")
    
    def create_hex_view(self, tokens: List[int]) -> Panel:
        """Create a hex view of tokens"""
        hex_text = Text()
        
        for i, token in enumerate(tokens):
            if i > 0 and i % 8 == 0:
                hex_text.append("\n")
            elif i > 0:
                hex_text.append(" ", style="dim")
            
            # Color based on token type
            decoded, token_type, _ = self.decode_token(token)
            hex_str = f"{token:06X}"
            
            if token_type == "SPECIAL":
                hex_text.append(hex_str, style="bold red")
            elif token_type == "ROLE":
                hex_text.append(hex_str, style="bold yellow")
            elif token_type == "CHANNEL":
                hex_text.append(hex_str, style="bold magenta")
            elif token_type == "TEXT":
                hex_text.append(hex_str, style="green")
            else:
                hex_text.append(hex_str, style="dim")
        
        return Panel(hex_text, title="🔢 Hex View", border_style="cyan")
    
    def visualize(self, message: str, include_system: bool = False, view_mode: str = "full"):
        """Main visualization method"""
        console.print("\n" + "="*80)
        console.print("[bold cyan]🎨 HARMONY TOKEN VISUALIZER - ENHANCED[/bold cyan]", justify="center")
        console.print("="*80 + "\n")
        
        # Create conversation
        messages = []
        if include_system:
            messages.extend([
                Message.from_role_and_content(Role.SYSTEM, SystemContent.new()),
                Message.from_role_and_content(
                    Role.DEVELOPER,
                    DeveloperContent.new().with_instructions("Be helpful and concise")
                )
            ])
        messages.append(Message.from_role_and_content(Role.USER, message))
        
        convo = Conversation.from_messages(messages)
        tokens = self.enc.render_conversation_for_completion(convo, Role.ASSISTANT)
        decoded = self.enc.decode_utf8(tokens)
        
        # Display based on view mode
        if view_mode == "full":
            # Full view with all visualizations
            console.print(f"[bold]Message:[/bold] {message}")
            console.print(f"[bold]Token Count:[/bold] {len(tokens)}")
            console.print(f"[bold]Token IDs:[/bold] {tokens}\n")
            
            # Flow diagram
            console.print(self.create_flow_diagram(tokens))
            console.print()
            
            # Detailed table
            console.print(self.create_detailed_table(tokens))
            console.print()
            
            # Tree view and statistics side by side
            tree = self.create_token_tree(tokens)
            stats = self.create_statistics_panel(tokens, message)
            
            console.print(Columns([
                Panel(tree, title="🌳 Structure", border_style="blue"),
                stats
            ]))
            
            # Hex view
            console.print()
            console.print(self.create_hex_view(tokens))
            
            # Decoded output
            console.print()
            console.print(Panel(
                decoded,
                title="📜 Decoded Output",
                border_style="green"
            ))
            
        elif view_mode == "compact":
            # Compact view
            console.print(f"[bold]Message:[/bold] {message}")
            console.print(f"[bold]Tokens:[/bold] {len(tokens)} total")
            console.print(self.create_flow_diagram(tokens))
            
        elif view_mode == "tree":
            # Tree view only
            console.print(self.create_token_tree(tokens))
            
        elif view_mode == "hex":
            # Hex view only
            console.print(self.create_hex_view(tokens))
            
        elif view_mode == "stats":
            # Statistics only
            console.print(self.create_statistics_panel(tokens, message))

def main():
    """Enhanced main with more options"""
    parser = argparse.ArgumentParser(
        description="Harmony Token Visualizer - See how text becomes tokens",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
View Modes:
  full     - Complete visualization with all views
  compact  - Simplified flow diagram only  
  tree     - Hierarchical structure view
  hex      - Hexadecimal token view
  stats    - Statistics only

Examples:
  %(prog)s "Hello world!"                    # Visualize a message
  %(prog)s --mode compact "Test"             # Compact view
  %(prog)s --system "Hi"                     # Include system messages
  %(prog)s --interactive                     # Interactive mode
        """
    )
    
    parser.add_argument(
        "message",
        nargs="*",
        help="Message to tokenize"
    )
    parser.add_argument(
        "--mode",
        choices=["full", "compact", "tree", "hex", "stats"],
        default="full",
        help="Visualization mode"
    )
    parser.add_argument(
        "--system",
        action="store_true",
        help="Include system and developer messages"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode with examples"
    )
    
    args = parser.parse_args()
    
    visualizer = TokenVisualizer()
    
    if args.interactive or not args.message:
        # Interactive mode
        examples = [
            "Hello!",
            "What's 2+2?",
            "Write Python code",
            "🎉 Celebration!",
            "Multi\nline\ntext",
            "System.out.println(\"Hello\");",
        ]
        
        console.print("[bold]Choose an example or enter custom:[/bold]")
        for i, ex in enumerate(examples, 1):
            console.print(f"  {i}. {ex[:30]}..." if len(ex) > 30 else f"  {i}. {ex}")
        console.print("  0. Enter custom message")
        console.print()
        
        choice = console.input("[bold]Choice:[/bold] ").strip()
        
        if choice == "0":
            message = console.input("[bold]Enter message:[/bold] ")
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            message = examples[int(choice)-1]
        else:
            message = "Hello!"
        
        # Ask for view mode
        console.print("\n[bold]View mode:[/bold]")
        console.print("  1. Full (all visualizations)")
        console.print("  2. Compact (flow only)")
        console.print("  3. Tree (structure)")
        console.print("  4. Hex (token values)")
        console.print("  5. Stats (statistics)")
        
        mode_choice = console.input("\n[bold]Mode:[/bold] ").strip()
        modes = ["full", "full", "compact", "tree", "hex", "stats"]
        view_mode = modes[int(mode_choice)] if mode_choice.isdigit() and 0 <= int(mode_choice) <= 5 else "full"
        
        visualizer.visualize(message, args.system, view_mode)
    else:
        # Command line mode
        message = " ".join(args.message)
        visualizer.visualize(message, args.system, args.mode)
    
    console.print("\n[dim]Try: python token_visualizer.py --help for more options[/dim]")

if __name__ == "__main__":
    main()