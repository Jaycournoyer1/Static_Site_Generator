class HTMLNode:
    """Base HTML node that stores shared element data and helper behavior."""

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # HTML tag name, e.g. "p", "a", "div".
        self.value = value  # Raw text/value for leaf-like nodes.
        self.children = children  # Child nodes for parent/container nodes.
        self.props = props  # Optional HTML attributes, e.g. {"href": "..."}.

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")  # Subclasses must implement.

    def props_to_html(self):
        """Serialize attribute dictionary into HTML attribute text."""
        if not self.props:  # If there are no attributes, return an empty suffix.
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())  # Build: key="value".

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"  # Debug view.


class LeafNode(HTMLNode):
    """HTML node with no children, represented by a tag/value pair."""

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)  # Force children to None for leaf nodes.

    def to_html(self):
        """Render this leaf node into an HTML string."""
        if self.value is None:  # Leaf nodes must always hold a value.
            raise ValueError("invalid HTML: no value")

        if self.tag is None:  # Plain text node without a wrapping HTML tag.
            return str(self.value)

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"  # Normal tagged element.

    def __repr__(self):
        return f"LeafNode(tag={repr(self.tag)}, value={repr(self.value)}, props={repr(self.props)})"  # Debug view.


class ParentNode(HTMLNode):
    """HTML node that wraps one or more child nodes inside a parent tag."""

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)  # Parent nodes do not hold direct text values.

    def to_html(self):
        """Render this parent node and all descendants into HTML."""
        if self.tag is None:  # Parent nodes must have a wrapping HTML tag.
            raise ValueError("invalid HTML: no tag")

        if self.children is None:  # Parent nodes must have child node(s) to render.
            raise ValueError("invalid HTML: no children")

        children_html = ""  # Accumulate rendered HTML from each child in order.
        for child in self.children:
            children_html += child.to_html()  # Recursively render each child node.

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"  # Wrap children in parent tag.

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"  # Debug view.
