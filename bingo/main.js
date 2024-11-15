BOARD = [];//穴が空いているの場所を表す
WEIGHT = 5//横
HEIGHT = 5//縦
NUM = [];//数字を格納する
REACH_COLUMN = [];//縦に見たときにリーチの場所を示す
REACH_ROW = [];//横に見たときにリーチの場所を示す
REACH= [];//リーチの場所を表す

//ボード生成
for (var i = 0; i < HEIGHT; i++) {
    BOARD[i] = [];
    REACH_COLUMN[i] = [];
    REACH_ROW[i] = [];
    NUM[i] = [];
    for (var j = 0; j < WEIGHT; j++) {
        BOARD[i][j] = false;
        REACH_COLUMN[i][j] = false;
        REACH_ROW[i][j] = false;
        NUM[i][j] = 0;
    }
}
function set_board(nums) {
    is_half = 0;
    for (var i = 0; i < HEIGHT; i++) {
        temp = [];
        for (var j = 0; j < WEIGHT; j++) {
            if (i * 5 + j == 12) {
                temp[j] = 'FREE';
                is_half = 1;
                continue;
            }
            // logger.log(i*5+j);
            temp[j] = nums[i * 5 + j - is_half];
        }
        NUM[i] = temp;
    }
    // NUM.insert(2, 'FREE');
}

function split_query(query) {
    result = []
    for (var i = 0; i < query.length; i++) {
        if (i % 2 == 1) {
            result[(i - 1) / 2] = query.substring(i - 1, i + 1)
        }
    }
    return result;
}

function decode_num(key) {
    alp = "abcdefghijklmnopqrstuvwxyz";
    return (alp.indexOf(key[0])) * 26 + alp.indexOf(key[1]);
}

function decode_query(query) {
    result = []
    for (var i = 0; i < query.length; i++) {
        result[i] = decode_num(query[i])
    }
    return result;
}

function switch_cell(id) {
    td = document.getElementById(id);
    if (td.classList.contains("bingo-cell-open")) {
        close_cell(td);
    } else {
        open_cell(td);
    }
    load_reach();
    td.onclick = function () { return switch_cell(this.id) };
}

function open_cell(td) {
    console.log("aaaaa<", td)
    pos = convert_pos_from_id(parseInt(td.id))
    BOARD[pos[0]][pos[1]] = true;
    // console.log(td)
    td.classList.add("bingo-cell-open");
}

function close_cell(td) {
    console.log("bbbb>", td)
    pos = convert_pos_from_id(parseInt(td.id))
    BOARD[pos[0]][pos[1]] = false;
    // console.log(td)
    td.classList.remove("bingo-cell-open");
}

function convert_pos_from_id(id) {
    return [Math.floor(id / 5), id % 5]
}



function check_bingo() {
    bingo = 0
    for (var i = 0; i < HEIGHT; i++) {
        is_bingo = true;//ビンゴかどうかを確認するための変数
        for (var j = 0; j < WEIGHT; j++) {
            is_bingo = BOARD[i][j] & is_bingo
        }
        if (is_bingo) {
            bingo++;
        }
    }
    for (var i = 0; i < WEIGHT; i++) {
        is_bingo = true;//ビンゴかどうかを確認するための変数
        for (var j = 0; j < HEIGHT; j++) {
            is_bingo = BOARD[j][i] & is_bingo
        }
        if (is_bingo) {
            bingo++;
        }
    }
    return bingo
}

function check_reach() {//リーチかどうかのチェック
    for (var i = 0; i < HEIGHT; i++) {//縦のチェック
        push_count = 0;
        for (var j = 0; j < WEIGHT; j++) {
            REACH_COLUMN[i][j] = false;
            if (BOARD[i][j]) {
                push_count++;
            }
        }
        for (var j = 0; j < WEIGHT; j++) {
            if (push_count == 4 && BOARD[i][j] == false) {
                REACH_COLUMN[i][j] = true;
            }
        }
    }
    for (var i = 0; i < WEIGHT; i++) {//横のチェック
        push_count = 0;
        for (var j = 0; j < HEIGHT; j++) {
            REACH_ROW[j][i] = false;
            if (BOARD[j][i]) {
                push_count++;
            }
        }
        for (var j = 0; j < HEIGHT; j++) {
            if (push_count == 4 && BOARD[j][i] == false) {
                REACH_ROW[j][i] = true;
            }
        }
    }
    for (var i = 0; i < HEIGHT; i++) {
        for (var j = 0; j < WEIGHT; j++) {
            if (REACH_COLUMN[i][j] || REACH_ROW[i][j]) {
                REACH[i][j] = true;
            } else {
                REACH[i][j] = false;
            }
        }
    }

}
function get_query() {
    var query = window.location.search;
    var queries = query.split('&');
    var result = {};
    for (var i = 0; i < queries.length; i++) {
        var query = queries[i].split('=');
        result[query[0]] = query[1];
    }
    return result;
}
function make_table() {
    var table = document.createElement('table');
    table.className = 'bingo-card';
    for (var i = 0; i < HEIGHT; i++) {
        var tr = document.createElement('tr');
        // tr.className="bingo-card"
        for (var j = 0; j < WEIGHT; j++) {
            var td = document.createElement('td');
            td.textContent = NUM[i][j];
            td.className = "bingo-cell"
            td.id = i * 5 + j
            // td.style.backgroundColor = '#FF0000'
            td.onclick = function () { switch_cell(this.id, true) };
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
    var card = document.getElementById('bingo-card-outline');
    card.after(table);
}

function load_reach() {
    // table=document.getElementById("bingo-card");
    check_reach()
    console.log(REACH_COLUMN[0])
    console.log(REACH_COLUMN[1])
    console.log(REACH_COLUMN[2])
    console.log(REACH_COLUMN[3])
    console.log(REACH_COLUMN[4])
    for (var i = 0; i < HEIGHT; i++) {
        for (var j = 0; j < WEIGHT; j++) {
            if (BOARD[i][j]) {
                // if (td.classList.contains("bingo-cell-reach")) {
                    // document.getElementById(i * 5 + j).classList.remove("bingo-cell-reach");
                // }
            } else {
                td = document.getElementById(i * 5 + j)
                if (REACH_COLUMN[i][j]) {
                    td.classList.add("bingo-cell-reach");
                    // table.rows[i].cells[j].classList.add("bingo-cell-reach");
                }
                else if (REACH_COLUMN[i][j] == false && td.classList.contains("bingo-cell-reach")) {
                    td.classList.remove("bingo-cell-reach");
                    // table.rows[i].cells[j].classList.remove("bingo-cell-reach");
                }
            }
        }
    }
}

// nums = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x']
query = get_query()
// set_board(nums["?card"])
// query=decode_cell(query)
if (query["?card"] == undefined) {
    query["?card"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
}
nums = split_query(query["?card"]);
nums = decode_query(nums)
set_board(nums)
make_table(nums)


