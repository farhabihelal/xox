use rand::rng;
use rand::seq::IteratorRandom;
use std::collections::HashSet;
use std::usize;

use pyo3::prelude::*;

#[derive(Copy, Clone, PartialEq)]
enum Player {
    Human,
    AI,
    Empty,
}

#[pyfunction]
pub fn get_best_move(board: Vec<i32>) -> usize {
    let mut board_internal = [Player::Empty; 9];
    for (i, &v) in board.iter().enumerate() {
        board_internal[i] = match v {
            1 => Player::Human,
            2 => Player::AI,
            _ => Player::Empty,
        };
    }
    // println!("[ original board ]");
    // display_board(&board_internal);
    // println!("\n");
    best_move(&mut board_internal)
}

fn is_winner(board: &[Player; 9], player: Player) -> bool {
    let wins = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ];
    wins.iter()
        .any(|line| line.iter().all(|&i| board[i] == player))
}

fn is_draw(board: &[Player; 9]) -> bool {
    board.iter().all(|&x| x != Player::Empty)
}

fn calc_minimax_value(depth: i32) -> i32 {
    10_000_000 / 10i32.pow((depth.min(5)) as u32)
}

fn minimax(board: &mut [Player; 9], is_maximizing: bool, depth: i32) -> i32 {
    if is_winner(board, Player::AI) {
        return calc_minimax_value(depth);
    }
    if is_winner(board, Player::Human) {
        let score = calc_minimax_value(depth) - 1;
        return if is_maximizing { -score } else { score };
    }
    if is_draw(board) {
        return 0;
    }

    let mut best_score = if is_maximizing { i32::MIN } else { i32::MAX };
    // let mut best_depth: i32 = i32::MAX;

    for i in 0..9 {
        if board[i] == Player::Empty {
            board[i] = if is_maximizing {
                Player::AI
            } else {
                Player::Human
            };
            // debug
            // if is_maximizing {
            //     println!("AI played: {},{}", i / 3, i % 3);
            // } else {
            //     println!("Human played: {},{}", i / 3, i % 3);
            // }
            // display_board(board, i / 3, i % 3);
            let score = minimax(board, !is_maximizing, depth + 1);

            // println!("------------------------------");
            // println!("Score={score}\nDepth={depth}");
            // println!("------------------------------");

            board[i] = Player::Empty;

            let is_better = if is_maximizing {
                score > best_score
            } else {
                score < best_score
            };

            if is_better {
                best_score = score;
                // best_depth = depth;
                // println!("Best score updated to {best_score}.\n")
            }
            // println!("\n");
        }
    }

    best_score
}

fn best_move(board: &mut [Player; 9]) -> usize {
    let mut best_score = i32::MIN;
    let mut candidate_indices: HashSet<usize> = HashSet::new();

    for i in 0..9 {
        if board[i] == Player::Empty {
            board[i] = Player::AI;

            // println!("------------------------------");
            // println!("[ FINDING BEST AI MOVE ]");
            // println!("------------------------------\n\n");
            // println!("AI played: {},{}", i / 3, i % 3);
            // display_board(board, i / 3, i % 3);
            let score = minimax(board, false, 1);

            // println!("###############################");
            // println!("Score={score}");
            // println!("###############################\n\n");

            board[i] = Player::Empty;

            if score > best_score {
                best_score = score;
                candidate_indices.clear();
                candidate_indices.insert(i);
                // println!("New Best score={best_score}.\n")
            } else if score == best_score {
                candidate_indices.insert(i);
            }

            // println!("\n\n\n\n\n\n\n\n\n");
        }
    }

    candidate_indices.into_iter().choose(&mut rng()).unwrap()
}

fn display_board(board: &[Player; 9], mark_row: usize, mark_col: usize) {
    println!("   0   1   2");
    for row in 0..3 {
        print!("{} ", row);
        for col in 0..3 {
            let i = row * 3 + col;
            let symbol = match board[i] {
                Player::Human => "X",
                Player::AI => "O",
                Player::Empty => " ",
            };
            if row == mark_row && col == mark_col {
                print!("<{}>", symbol);
            } else {
                print!(" {} ", symbol);
            }
            if col != 2 {
                print!("|");
            }
        }
        println!();
        if row != 2 {
            println!("  ---+---+---");
        }
    }
    println!();
}

#[pymodule]
fn xox_ai(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_best_move, m)?)?;
    Ok(())
}
