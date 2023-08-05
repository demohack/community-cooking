"use strict"
// uniqlo code  UQ20-CWRBBHQT5ZXX
/** Connect Four
 *
 * Player 1 and 2 alternate turns. On each turn, a piece is dropped down a
 * column until a player gets four-in-a-row (horiz, vert, or diag) or until
 * board fills (tie)
 */

const WIDTH = 6;
const HEIGHT = 6;

let board = undefined; // array of rows, each row is array of cells  (board[y][x])
let htmlBoard = undefined;
let columnTop = undefined;

function getHtmlBoard() {
    if (htmlBoard == undefined) {
        htmlBoard = document.querySelector("#board");
    }
    return htmlBoard;
}
class Player {
    constructor(playerNumber, playerScore = 0) {
        this.number = playerNumber;
        this.color = playerNumber == 1 ? "blue" : "red";
        this.score = playerScore;
    }

    addScore() {
        this.score = this.score + 1;
    }

    updateScore() {
        let html = document.querySelector(`#${this.color}Score`);
        html.innerHTML = `player ${this.number}: ${this.score}`;
    }

    unsetTopClass() {
        columnTop.classList.remove(`player-${this.number}`);
    }

    setTopClass() {
        columnTop.classList.add(`player-${this.number}`);
    }
}

class Game {
    constructor() {
        this.gameWon = false;
        this.gameTied = false;
        this.clickInProgress = false;

        this.player1 = new Player(1);
        this.player2 = new Player(2);

        this.currPlayer = this.player1;
        this.startPlayer = this.player1;
    }

    getCurrentPlayer() {
        return this.currPlayer;
    }

    setCurrentPlayer(newPlayer) {
        return this.currPlayer = newPlayer;
    }

    switchCurrent() {
        return this.currPlayer = this.currPlayer.number == 1 ? this.player2 : this.player1;
    }

    getStartPlayer() {
        return this.startPlayer;
    }

    setStartPlayer(newPlayer) {
        return this.startPlayer = newPlayer;
    }

    switchStart() {
        return this.startPlayer = this.startPlayer.number == 1 ? this.player2 : this.player1;
    }

    clearGameCondition() {
        this.gameWon = false;
        this.gameTied = false;
        this.clickInProgress = false;
    }

    setClickInProgress() {
        this.clickInProgress = true;
    }

    unsetClickInProgress() {
        this.clickInProgress = false;
    }

    getGamePause() {
        return this.gameWon || this.gameTied || this.clickInProgress;
    }
}

let game = new Game();

/** makeBoard: create in-JS board structure:
 *    board = array of rows, each row is array of cells  (board[y][x])
 */

function makeBoard() {
    // set "board" to empty HEIGHT x WIDTH matrix array

    board = [];
    board.length = HEIGHT;

    for (let i = 0; i < HEIGHT; i++) {
        let cells = [];
        cells.length = WIDTH;

        board[i] = cells;
    }
}

function deleteHtmlBoard() {
    // get "htmlBoard" variable from the item in HTML w/ID of "board"
    getHtmlBoard().innerHTML = "";
}

/** makeHtmlBoard: make HTML table and row of column tops. */

function makeHtmlBoard() {
    // get "htmlBoard" variable from the item in HTML w/ID of "board"
    let htmlBoard = getHtmlBoard();

    htmlBoard.append(makeColumnTop());

    // create the HTML game board for given HEIGHT and WIDTH
    for (let y = 0; y < HEIGHT; y++) {
        const row = document.createElement("tr");
        for (let x = 0; x < WIDTH; x++) {
            const td = document.createElement("td");
            td.id = `d-${HEIGHT - y - 1}-${x}`;

            let div = document.createElement("div");
            div.classList.add("piece");

            td.append(div);
            row.append(td);
        }
        htmlBoard.append(row);
    }
}

// create the table header row "column top"
function makeColumnTop() {
    // create the table header row "column top"
    let top = document.createElement("tr");
    top.id = "column-top";
    top.addEventListener("click", handleClick);

    for (let x = 0; x < WIDTH; x++) {
        let td = document.createElement("td");
        td.id = `h-${x}`;

        let div = document.createElement("div");
        div.classList.add("top-piece");
        td.append(div);

        top.append(td);
    }

    return columnTop = top;
}

/** findSpotForCol: given column x, return top empty y (null if filled) */

function findSpotForCol(x) {
    for (let y = 0; y < HEIGHT; y++) {
        if (board[y][x] == undefined) {
            return y;
        }
    }

    return null;
}

/** placeInTable: update DOM to place piece into HTML table of board */

function placeInTable(y, x, player, callback) {
    // add line to update in-memory board
    board[y][x] = player;

    // get top div
    let topDiv = htmlBoard.querySelector(`#h-${x} div`);
    if (topDiv == null) {
        callback();
        return false;
    }

    // animate drop piece
    topDiv.classList.add("drop-piece");
    topDiv.style.backgroundColor = game.getCurrentPlayer().color;
    topDiv.style.top = `${66 * (HEIGHT - y)}px`;

    // wait 2 seconds, and then...
    setTimeout(function () {
        let cn = `player-${game.getCurrentPlayer().number}-piece`;

        // reset top div
        topDiv.classList.remove("drop-piece");
        topDiv.style.backgroundColor = "";

        // make a div and insert into correct table cell
        let div = htmlBoard.querySelector(`#d-${y}-${x} div`);
        div.classList.add(cn);

        callback();
    }, 2000);
}

function updateResult(msg) {
    let htmlResult = document.querySelector("#result");
    htmlResult.innerHTML = msg;
}

/** handleClick: handle click of column top to play piece */

function handleClick(evt) {
    // exit if game has been won or is tied
    if (game.getGamePause()) {
        return;
    }
    game.setClickInProgress();

    // get x from ID of clicked cell
    let id = evt.target.parentElement.id;
    let idx = id.indexOf("-") + 1;
    let x = +id.substring(idx, id.length); // single + operator converts string to number

    // get next spot in column (if none, ignore click)
    let y = findSpotForCol(x);
    if (y === null) {
        game.unsetClickInProgress();
        return;
    }

    let player = game.getCurrentPlayer();
    player.unsetTopClass();

    placeInTable(y, x, player.number, function () {
        game.unsetClickInProgress();

        if (checkForWin(player.number)) {
            game.gameWon = true;
            player.addScore();
            player.updateScore();
            return updateResult(`player ${player.number} won!`);
        }

        if (checkForTie()) {
            game.gameTied = true;
            return updateResult(`game tied!`);
        }

        game.switchCurrent().setTopClass();
    });
}

/** checkForWin: check board cell-by-cell for "does a win start here?" */

function checkForTie() {
    let x = undefined;
    let y = HEIGHT - 1;

    for (x = 0; x < WIDTH; x++) {
        if (board[y][x] == undefined) {
            return false;
        }
    }

    return true;
}

function checkForWin(player) {
    function _win(cells) {
        // Check four cells to see if they're all color of current player
        //  - cells: list of four (y, x) cells
        //  - returns true if all are legal coordinates & all match currPlayer

        return cells.every(
            ([y, x]) =>
            y >= 0 &&
            y < HEIGHT &&
            x >= 0 &&
            x < WIDTH &&
            board[y][x] === player
        );
    }

    // modified code to be a little more efficient:
    // no need to iterate to the end of height or width
    // because we're also creating temporary arrays to look ahead
    // to determine win conditions
    for (let y = 0; y < HEIGHT; y++) {
        for (let x = 0; x < WIDTH; x++) {
            // create a temporary array from horizontal cells
            let horiz = [
                [y, x],
                [y, x + 1],
                [y, x + 2],
                [y, x + 3]
            ];

            // create a temporary array from vertical cells
            let vert = [
                [y, x],
                [y + 1, x],
                [y + 2, x],
                [y + 3, x]
            ];

            // create a temporary array from diagonal right cells
            let diagDR = [
                [y, x],
                [y + 1, x + 1],
                [y + 2, x + 2],
                [y + 3, x + 3]
            ];

            // create a temporary array from diagonal left cells
            let diagDL = [
                [y, x],
                [y + 1, x - 1],
                [y + 2, x - 2],
                [y + 3, x - 3]
            ];

            // check if any of the temporary arrays meet the win condition
            if (_win(horiz) || _win(vert) || _win(diagDR) || _win(diagDL)) {
                return true;
            }
        }
    }
}

function setRestartButton() {
    // get "htmlBoard" variable from the item in HTML w/ID of "board"
    let button = document.querySelector("#restartButton");
    button.addEventListener("click", restartButtonClick);
}

function restartButtonClick() {
    deleteHtmlBoard();
    makeHtmlBoard();
    makeBoard();
    game.clearGameCondition();
    game.switchStart().setTopClass();
    updateResult(`player ${game.getCurrentPlayer().number} to start`);
}

setRestartButton();
makeHtmlBoard();
makeBoard();
game.clearGameCondition();
game.setCurrentPlayer(game.player1).setTopClass();
updateResult(`player ${game.getCurrentPlayer().number} to start`);
game.player1.updateScore();
game.player2.updateScore();