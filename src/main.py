from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    #node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(node)
    node = HTMLNode("p", "hello", None, None)
    print(node)

    

    
if __name__ == "__main__":
    main()