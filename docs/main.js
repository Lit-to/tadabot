BOARD = [];//穴が空いているの場所を表す
SIDES = 5//横
SIDES = 5//縦
NUM = [];//数字を格納する
REACH_COLUMN = [];//縦に見たときにリーチの場所を示す
REACH_ROW = [];//横に見たときにリーチの場所を示す
REACH = [];//リーチの場所を表す

//ボード生成
for (var i = 0; i < SIDES; i++) {
    BOARD[i] = [];
    REACH_COLUMN[i] = [];
    REACH_ROW[i] = [];
    REACH[i] = [];
    NUM[i] = [];
    for (var j = 0; j < SIDES; j++) {
        BOARD[i][j] = false;
        REACH_COLUMN[i][j] = false;
        REACH_ROW[i][j] = false;
        REACH[i][j] = false;
        NUM[i][j] = 0;
    }
}
function set_board(nums) {
    is_half = 0;
    for (var i = 0; i < SIDES; i++) {
        temp = [];
        for (var j = 0; j < SIDES; j++) {
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
    is_bingo=true
    for (var i = 0; i < SIDES; i++) {
        is_bingo = true;//ビンゴかどうかを確認するための変数
        for (var j = 0; j < SIDES; j++) {
            is_bingo = BOARD[i][j] & is_bingo
        }
        if (is_bingo) {
            bingo++;
        }
    }
    for (var i = 0; i < SIDES; i++) {
        is_bingo = true;//ビンゴかどうかを確認するための変数
        for (var j = 0; j < SIDES; j++) {
            is_bingo = BOARD[j][i] & is_bingo
        }
        if (is_bingo) {
            bingo++;
        }
    }
    is_bingo=true;
    for (var i=0;i<SIDES;i++){
        is_bingo=BOARD[i][i]&is_bingo
    }
    if (is_bingo) {
        bingo++;
    }
    is_bingo=true;
    for (var i=0;i<SIDES;i++){
        is_bingo=BOARD[i][SIDES-i-1]&is_bingo
    }
    if (is_bingo) {
        bingo++;
    }
    return bingo
}

function check_reach() {//リーチかどうかのチェック
    for (var i = 0; i < SIDES; i++) {//縦のチェック
        push_count = 0;
        for (var j = 0; j < SIDES; j++) {
            REACH[i][j] = false;
            if (BOARD[i][j]) {
                push_count++;
            }
        }
        for (var j = 0; j < SIDES; j++) {
            if (push_count == 4 && BOARD[i][j] == false) {
                REACH[i][j] = true;
            }
        }
    }
    for (var i = 0; i < SIDES; i++) {//横のチェック
        push_count = 0;
        for (var j = 0; j < SIDES; j++) {
            // REACH_ROW[j][i] = false;
            if (BOARD[j][i]) {
                push_count++;
            }
        }
        for (var j = 0; j < SIDES; j++) {
            if (push_count == 4 && BOARD[j][i] == false) {
                REACH[j][i] = true;
            }
        }
    }
    push_count = 0;
    for (var i = 0; i < SIDES; i++) {
        if (BOARD[i][i]) {
            push_count++;
        }
    }
    for (var i = 0; i < SIDES; i++) {
        if (push_count == 4 && BOARD[i][i] == false) {
            REACH[i][i] = true;
        }
    }
    push_count = 0;
    for (var i = 0; i < SIDES; i++) {
        if (BOARD[i][SIDES-i-1]) {
            push_count++;
        }
    }
    for (var i = 0; i < SIDES; i++) {
        if (push_count == 4 && BOARD[SIDES-i-1][i] == false) {
            REACH[SIDES-i-1][i] = true;
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
function make_table(name) {
    var table = document.createElement('table');
    table.className = 'bingo-card';
    for (var i = 0; i < SIDES; i++) {
        var tr = document.createElement('tr');
        // tr.className="bingo-card"
        for (var j = 0; j < SIDES; j++) {
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
    document.getElementById("name").textContent = name;
    card.after(table);
}

function load_reach() {
    // table=document.getElementById("bingo-card");
    check_reach()
    for (var i = 0; i < SIDES; i++) {
        for (var j = 0; j < SIDES; j++) {
            if (BOARD[i][j]) {
                // if (td.classList.contains("bingo-cell-reach")) {
                // document.getElementById(i * 5 + j).classList.remove("bingo-cell-reach");
                // }
            } else {
                td = document.getElementById(i * 5 + j)
                if (REACH[i][j]) {
                    td.classList.add("bingo-cell-reach");
                    // table.rows[i].cells[j].classList.add("bingo-cell-reach");
                }
                else if (REACH[i][j] == false && td.classList.contains("bingo-cell-reach")) {
                    td.classList.remove("bingo-cell-reach");
                    // table.rows[i].cells[j].classList.remove("bingo-cell-reach");
                }
            }
        }
    }
}

function switch_cell(id) {
    td = document.getElementById(id);
    if (td.classList.contains("bingo-cell-open")) {
        close_cell(td);
    } else {
        open_cell(td);
    }
    load_reach();
    bingo = check_bingo();
    p=document.getElementById("bingo-count");
    p.textContent=bingo+" BINGO!!";
    td.onclick = function () { return switch_cell(this.id) };
}

function set_icon(icon){
    document.getElementById("icon").src=icon;
}


query = get_query()
if (query["?card"] == undefined) {
    query["?card"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
}
if (query["?icon"] == undefined) {
    query["?icon"] = "https://cdn.discordapp.com/attachments/379156047253733409/1309918751046504538/egg_step_4.png?ex=67435467&is=674202e7&hm=a6fa9721597830855144da386c65994ea27293b6178c70b4890f1a85608cd423&"
}
user_name=decodeURI(query["?name"])
user_name=user_name.substring(0,7)
if (user_name == undefined) {
    user_name = "無名たこ焼き"
}
set_icon(query["?icon"])
nums = split_query(query["?card"]);
nums = decode_query(nums)
set_board(nums)
make_table(user_name)


