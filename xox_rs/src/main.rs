mod xox_ai;

fn main() {
    // let board: Vec<i32> = vec![0, 0, 2, 0, 1, 0, 1, 0, 2];
    let board: Vec<i32> = vec![1, 0, 2, 0, 2, 0, 1, 0, 1];
    let idx = xox_ai::get_best_move(board);
    println!("{idx}");
}
