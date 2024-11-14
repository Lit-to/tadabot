BOARD = [];
WEIGHT = 5
HEIGHT = 5
NUM = [];
REACH = [];

//ボード生成
for (var i = 0; i < HEIGHT; i++) {
    BOARD[i] = [];
    REACH[i] = [];
    NUM[i] = [];
    for (var j = 0; j < WEIGHT; j++) {
        BOARD[i][j] = false;
        REACH[i][j] = false;
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

function switch_cell(id){
    td=document.getElementById(id);
    if (td.classList.contains("bingo-cell-open")) {
        close_cell(td);
    }else{
        open_cell(td);
    }
    td.onclick=function(){return switch_cell(this.id)};
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

function convert_pos_from_id(id){
    return [Math.floor(id/5),id%5]
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

function check_reach() {
    REACH = [];
    for (var i = 0; i < HEIGHT; i++) {
        push_count = 0;
        for (var j = 0; j < WEIGHT; j++) {
            if (BOARD[i][j]) {
                push_count++;
                REACH[i][j] = false;
            }
        }
        for (var j = 0; j < WEIGHT; j++) {
            if (push_count == 4) {
                REACH[i][j] = true;
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
function makeTable() {
    var table = document.createElement('table');
    table.className = 'bingo-card';
    for (var i = 0; i < HEIGHT; i++) {
        var tr = document.createElement('tr');
        // tr.className="bingo-card"
        for (var j = 0; j < WEIGHT; j++) {
            var td = document.createElement('td');
            td.textContent = NUM[i][j];
            td.className = "bingo-cell"
            td.id=i*5+j
            // td.style.backgroundColor = '#FF0000'
            td.onclick = function(){switch_cell(this.id,true)};
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }
    var card = document.getElementById('bingo-card');
    card.after(table);
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
makeTable(nums)


