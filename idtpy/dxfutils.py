import ezdxf
import numpy as np

class DxfAssistant():
    def __init__(self, doc = None, block_name='IDT'):
        if doc is None:
            self.doc = ezdxf.new("R2013")
        else:
            self.doc = doc
        self.msp = self.doc.modelspace()
        self.block_name=block_name
        self.block = self.doc.blocks.new(name=self.block_name)

    def save(self, fullpath):
        self.doc.saveas(fullpath)

    def add_idt_to_dxf(self, idt_design, pos, layer='IDT'):
        if layer not in self.doc.layers:
            self.doc.layers.add(name=layer, color=1)

        for pol in idt_design:
            points = np.array([[float(x), float(y)] for x, y in pol.vertices])*1e-3
            if not np.array_equal(points[0], points[-1]):
                points = np.vstack([points, points[0]])  # Close the polygon
            self.block.add_lwpolyline(points, dxfattribs={'layer': layer})

        self.msp.add_blockref(self.block_name, pos)