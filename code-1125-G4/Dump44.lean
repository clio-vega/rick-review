import TworowD4Kernel.PhiOut
open TworowD4Kernel.PhiOut TworowD4Kernel.PhiOutData TworowD4Kernel.SlideSwitch

/-- Print Φ and Σ∘rr as explicit maps on the R×C box: one line per instance. -/
def showOut (R C : ℕ) (o : Finset Cell × (Cell → ℕ)) : String :=
  let cells := (List.range R).flatMap fun r => (List.range C).map fun c => (r, c)
  String.intercalate " " ((cells.filter fun y => decide (y ∈ o.1)).map fun y =>
    s!"{y.1},{y.2}:{o.2 y}")

def dumpAll44 : IO Unit := do
  let mut i := 0
  for d in phiData44 do
    let (R, C, A, B, fl, _) := d
    IO.println s!"{i}|PHI|{showOut R C (phi R C A B (ofList fl))}|SIG|{showOut R C (sigmaRR R C A B (ofList fl))}"
    i := i + 1

#eval dumpAll44
