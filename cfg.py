from models import BasicBlock, CFG, RailProgram

CONDITIONAL_JUMPS = {'JG', 'JGE', 'JL', 'JLE', 'JE', 'JNE'}
JUMP_OPS = CONDITIONAL_JUMPS | {'JCC'}


def build_cfg(program: RailProgram) -> CFG:
    instructions = program.instructions
    count = len(instructions)

    leaders = {0}
    leaders.update(index for index in program.labels.values() if index < count)
    targets = {}

    for i, inst in enumerate(instructions):
        if inst.operation not in JUMP_OPS:
            continue
        label = inst.args[2]
        if label not in program.labels:
            raise ValueError(f'Переход ссылается на метку, которая не объявлена в программе')
        target = program.labels[label]
        if target >= count:
            raise ValueError(f'Метка существует, но после неё нет инструкций, к которым можно перейти')
        targets[i] = target
        leaders.add(target)
        if i + 1 < count:
            leaders.add(i + 1)

    starts = sorted(leaders)
    blocks = {}
    index_to_block = {}
    for block_id, start in enumerate(starts):
        end = starts[block_id + 1] if block_id + 1 < len(starts) else count
        blocks[block_id] = BasicBlock(block_id, start, instructions[start:end])
        for index in range(start, end):
            index_to_block[index] = block_id

    edges = {block_id: [] for block_id in blocks}

    def link(source_block, target_instruction):
        target_block = index_to_block[target_instruction]
        if target_block not in edges[source_block]:
            edges[source_block].append(target_block)

    for block_id, block in blocks.items():
        final_index = block.start + len(block.instructions) - 1
        final_inst = instructions[final_index]
        next_index = final_index + 1
        has_next = next_index < count

        if final_inst.operation in CONDITIONAL_JUMPS:
            link(block_id, targets[final_index])
            if has_next:
                link(block_id, next_index)
        elif final_inst.operation == 'JCC':
            condition = final_inst.args[0]
            if condition != '0':
                link(block_id, targets[final_index])
            if condition != '1' and has_next:
                link(block_id, next_index)
        elif has_next:
            link(block_id, next_index)

    return CFG(blocks=blocks, edges=edges, entry=0)
