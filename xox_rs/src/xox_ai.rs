use pyo3::prelude::*;

#[derive(Copy, Clone, PartialEq)]
enum Player {
    Human,
    AI,
    Empty,
}

#[pyfunction]
fn get_best_move(board: Vec<i32>) -> usize {
    let mut board_internal = [Player::Empty; 9];
    for (i, &v) in board.iter().enumerate() {
        board_internal[i] = match v {
            1 => Player::Human,
            2 => Player::AI,
            _ => Player::Empty,
        };
    }

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

fn minimax(board: &mut [Player; 9], is_maximizing: bool) -> i32 {
    if is_winner(board, Player::AI) {
        return 1;
    }
    if is_winner(board, Player::Human) {
        return -1;
    }
    if is_draw(board) {
        return 0;
    }

    let mut best_score = if is_maximizing { i32::MIN } else { i32::MAX };

    for i in 0..9 {
        if board[i] == Player::Empty {
            board[i] = if is_maximizing {
                Player::AI
            } else {
                Player::Human
            };
            let score = minimax(board, !is_maximizing);
            board[i] = Player::Empty;

            if is_maximizing {
                best_score = best_score.max(score);
            } else {
                best_score = best_score.min(score);
            }
        }
    }

    best_score
}

fn best_move(board: &mut [Player; 9]) -> usize {
    let mut best_score = i32::MIN;
    let mut move_index = 0;

    for i in 0..9 {
        if board[i] == Player::Empty {
            board[i] = Player::AI;
            let score = minimax(board, false);
            board[i] = Player::Empty;

            if score > best_score {
                best_score = score;
                move_index = i;
            }
        }
    }

    move_index
}

#[pymodule]
fn xox_ai(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_best_move, m)?)?;
    Ok(())
}
