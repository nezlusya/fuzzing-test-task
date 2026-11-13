from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    operation: str
    args: tuple[str, str, str]
    line: int
    def __str__(self) -> str:
        return f"{self.operation} {', '.join(self.args)}"

@dataclass
class RailProgram:
    instructions: list[Instruction]
    labels: dict[str, int]

@dataclass
class BasicBlock:
    id: int
    start: int
    instructions: list[Instruction]


@dataclass
class CFG:
    blocks: dict[int, BasicBlock]
    edges: dict[int, list[int]]
    entry: int
