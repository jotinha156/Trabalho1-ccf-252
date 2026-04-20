add x1, x0, x0
andi x2, x1, 10
L1: or x3, x1, x2
sll x4, x3, x1
sh x4, 8(x2)
lh x5, 8(x2)
bne x5, x0, L1