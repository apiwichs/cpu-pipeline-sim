class Instruction():
    def __init__(self, instruction: str, src_regs: tuple[str, ...], dst_reg: str | None):
        self.instruction = instruction
        self.src_regs = src_regs
        self.dst_reg = dst_reg
        
    def __str__(self):
        srcs = ",".join(self.src_regs)
        dst = self.dst_reg if self.dst_reg is not None else "-"
        return f"{self.instruction} {dst} <- {srcs}"
