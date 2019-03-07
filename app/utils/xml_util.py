from lxml import etree

def xml_to_map(source):
    xml = etree.fromstring(source, parser=etree.XMLParser(resolve_entities=False))
    return {sub_node.tag: sub_node.text for sub_node in xml}


def map_to_xml(data, root='xml', pretty=True):
    root = etree.Element(root)
    for key, value in data.items():
        child = etree.SubElement(root, key)
        child.text = str(value)
    return etree.tostring(root, pretty_print=pretty).decode(encoding='utf-8')



if __name__ == '__main__':
   pass