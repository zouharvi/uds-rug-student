fn main() {
    let run_h_count: Vec<i32> = vec![5, 9, 8, 4, 6];
    let mut params: Vec<f32> = vec![0.6, 0.4];
    let mut partial_counts: Vec<Vec<Vec<f32>>> = vec![vec![vec![0.0; 2]; 2]; 5];

    for i in 0..10 {
        println!("Step {}", i);

        // clear partial_counts
        for (run_i, run_h) in run_h_count.iter().enumerate() {
            partial_counts[run_i] = vec![vec![0.0; 2]; 2];
        }

        // expectation

        for (dice_i, dice_param) in params.iter().enumerate() {
            for (run_i, run_h) in run_h_count.iter().enumerate() {
                partial_counts[run_i][dice_i][0] += (*run_h as f32) * dice_param;
                partial_counts[run_i][dice_i][1] += ((10 - *run_h) as f32) * (1.0 - dice_param);
            }
        }
        for (run_i, run_h) in run_h_count.iter().enumerate() {
            for (dice_i, dice_param) in params.iter().enumerate() {
                let sum_dice: f32 = partial_counts[run_i].iter().map(|x| x[dice_i]).sum();
                let sum_all: f32 = partial_counts[run_i]
                    .iter()
                    .map(|x| x.iter().sum::<f32>())
                    .sum();
                partial_counts[run_i][dice_i][0] *= sum_dice / sum_all;
                partial_counts[run_i][dice_i][1] *= sum_dice / sum_all;
            }
        }

        // maximization
        for (dice_i, dice_param) in params.iter_mut().enumerate() {
            let partial_0: f32 = partial_counts.iter().map(|x| x[dice_i][0]).sum();
            let partial_1: f32 = partial_counts.iter().map(|x| x[dice_i][1]).sum();
            *dice_param = partial_0 / (partial_0 + partial_1);
        }

        println!("{:?}", params);
    }
}
