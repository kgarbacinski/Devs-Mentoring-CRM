class QuantityHandler {

    static DONE_EXERCISES = document.getElementsByClassName("done-tasks")[0]
    static ALL_EXERCISES = document.getElementsByClassName("all-tasks")[0]
    static WHOLE_PROGRESS_INFO = document.getElementsByClassName("student-info-progress p-3 mb-5")[0]
    static EXERCISE_TABLE = document.getElementsByClassName("tab-content")[0]
    static DONE_EASY_EXERCISES_QUANTITY = document.getElementsByClassName("done-easy")[0]
    static EASY_EXERCISES_QUANTITY = document.getElementsByClassName("total-easy")[0]
    static DONE_MEDIUM_EXERCISES_QUANTITY = document.getElementsByClassName("done-medium")[0]
    static MEDIUM_EXERCISES_QUANTITY = document.getElementsByClassName("total-medium")[0]
    static DONE_HARD_EXERCISES_QUANTITY = document.getElementsByClassName("done-hard")[0]
    static HARD_EXERCISES_QUANTITY = document.getElementsByClassName("total-hard")[0]

    static handle_quantity(quantity) {
        QuantityHandler.DONE_EXERCISES.textContent = quantity.done_exercises_quantity
        QuantityHandler.ALL_EXERCISES.textContent = quantity.all_exercises_quantity
        QuantityHandler.EASY_EXERCISES_QUANTITY.textContent = quantity.easy_exercises_quantity
        QuantityHandler.DONE_EASY_EXERCISES_QUANTITY.textContent = quantity.done_easy_exercises_quantity
        QuantityHandler.DONE_MEDIUM_EXERCISES_QUANTITY.textContent = quantity.done_medium_exercises_quantity
        QuantityHandler.MEDIUM_EXERCISES_QUANTITY.textContent = quantity.medium_exercises_quantity
        QuantityHandler.DONE_HARD_EXERCISES_QUANTITY.textContent = quantity.done_hard_exercises_quantity
        QuantityHandler.HARD_EXERCISES_QUANTITY.textContent = quantity.hard_exercises_quantity

    }

}


class ExercisesHandler {
    static EXERCISES_LIST_EASY = document.getElementsByClassName("tasks-list-box tasks-list-box-easy")[0]
    static EXERCISES_LIST_MEDIUM = document.getElementsByClassName("tasks-list-box tasks-list-box-medium")[0]
    static EXERCISES_LIST_HARD = document.getElementsByClassName("tasks-list-box tasks-list-box-hard")[0]

    static COLOR_HTML_DICT = {
        'easy': `<div class="level-color level-color-easy"></div>`,
        'medium': `<div class="level-color level-color-medium"></div>`,
        'hard': `<div class="level-color level-color-hard"></div>`

    }

    static EXERCISES_LIST_DICT = {
        'easy': ExercisesHandler.EXERCISES_LIST_EASY,
        'medium': ExercisesHandler.EXERCISES_LIST_MEDIUM,
        'hard': ExercisesHandler.EXERCISES_LIST_HARD
    }

    static clean_exercises_lists_html() {
        for (let key in ExercisesHandler.EXERCISES_LIST_DICT) {
            ExercisesHandler.EXERCISES_LIST_DICT[key].innerHTML = ""
        }
    }

    static create_exercise_html(exercise) {
        return `<a class="go-to-checker" href="#">
                                <div class="complete-box">
                                </div>
                                <div class="task-name">
                                    <span>${exercise.name}</span>
                                </div>
                            </a>`
    }


    static handle_all_exercises(exercises) {
        const keys = Object.keys(exercises);
        keys.forEach((key, index) => {
            this.handle_easy_exercises(key, exercises[key]);
        });
    }

    static handle_easy_exercises(exercises_type, exercises) {
        exercises.forEach(exercise => {
            Object.entries(exercise).forEach(([key, value]) => {
            });
            let main_div = document.createElement('div');
            main_div.className = "task-box mb-2";
            main_div.innerHTML = (this.create_exercise_html(exercise));
            let complete_box = main_div.getElementsByClassName("complete-box")[0]
            complete_box.innerHTML = (this.handle_status_div(exercise.done))
            this.handle_type_div(main_div, exercises_type)
            this.segregate_exercises_tables(exercises_type, main_div);

        });


    }

    static handle_status_div(status) {
        if (status) {
            return `<div class="complete-circle complete"></div>`
        } else {
            return `<div class="complete-circle"></div>`
        }


    }

    static handle_type_div(main_div, exercises_type) {
        let colour_div = document.createElement('div')
        let go_to_checker = main_div.getElementsByClassName("go-to-checker")[0]
        colour_div.innerHTML = ExercisesHandler.COLOR_HTML_DICT[exercises_type]
        go_to_checker.appendChild(colour_div)

    }

    static segregate_exercises_tables(exercises_type, main_div) {
        ExercisesHandler.EXERCISES_LIST_DICT[exercises_type].appendChild(main_div)

    }
}


async function getPathExercisesInfo(path_id) {
    ExercisesHandler.clean_exercises_lists_html()
    let url = (`${window.location.origin}/api/access/exercises/${path_id}`)
    let response = await fetch(url);
    if (response.ok) {
        let exercises_info = await response.json();
        QuantityHandler.handle_quantity(exercises_info.quantity);
        ExercisesHandler.handle_all_exercises(exercises_info.exercises);
        QuantityHandler.WHOLE_PROGRESS_INFO.style.visibility = "visible"
        QuantityHandler.EXERCISE_TABLE.style.visibility = "visible"
    }

}