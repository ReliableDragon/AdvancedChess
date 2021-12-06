
var pieces = {}; // id: dict(piece) + img_id
var highlighted_ids = [];
var highlighted_piece_id = null;
var change_interval;
var turn = 'white';

$(document).ready(function() {

  let clear_highlights = function() {
    for (const id of highlighted_ids) {
      $(`#${id}`).remove();
    }
    highlighted_ids = [];
    highlighted_piece_id = null;
  }

  let highlight_moves = function(piece_data) {
    return function() {
      console.log(piece_data);
      if (highlighted_piece_id != null) {
        if (highlighted_piece_id === piece_data.id) {
          clear_highlights();
          return;
        }
      }

      if (piece_data.color !== turn) {
        return;
      }

      // Nothing is already highlighted, so show moves.
      highlighted_piece_id = piece_data.id;
      let piece_coord = String(piece_data.row) + String(piece_data.col);
      $(`#square${piece_coord}`).append(`<div class=active_piece id="highlight${piece_data.id}"></div>`);
      highlighted_ids.push(`highlight${piece_data.id}`);

      for (const square of piece_data.valid_moves) {
        let x = square[0];
        let y = square[1];
        let target_id = String(x) + String(y);
        let highlight = $(`<div class=valid_move id="highlight${target_id}"></div>`);
        $(`#square${target_id}`).append(highlight);
        highlighted_ids.push(`highlight${target_id}`);
      }

      if (!("valid_attacks" in piece_data) || !piece_data.valid_attacks) {
        return;
      }
      for (const square of piece_data.valid_attacks) {
        let x = square[0];
        let y = square[1];
        let target_id = String(x) + String(y);
        let highlight = $(`<div class=valid_attack id="highlight${target_id}"></div>`);
        $(`#square${target_id}`).append(highlight);
        highlighted_ids.push(`highlight${target_id}`);
      }
    };
  }

  let build_board = function(height, width, pieces) {

    let board = $(".board");

    for (let i = 0; i < height; i++) {
      let row = $(`<div class="row" id="row${i}"></div>`);
      for (let j = 0; j < width; j++) {
        if ((i + j) % 2 == 0) {
          color = 'white';
        } else {
          color = 'black';
        }
        let square = $(`#${color}_root`).clone().attr('id', `square${i}${j}`);
        row.append(square);
      }
      board.append(row);
    }
    $("#row_root").remove();
  };

  let remove_img = function(existing_id) {
    let piece = pieces[existing_id];
    console.log(`Removing piece ${piece}.`)
    let img_id = piece.img_id;
    $(`#${img_id}`).remove();
    delete pieces[existing_id];
  }

  let add_img = function(new_piece) {
    let img_id = "img_" + new_piece.id;
    let img = $(`<img id=${img_id} class="piece" src=/static/imgs/${new_piece.icon}.png alt=${new_piece.icon}>`);
    let square = $(`#square${new_piece.row}${new_piece.col}`);
    square.append(img);
    square.click(highlight_moves(new_piece));
    new_piece.img_id = img_id;
    pieces[new_piece.id] = new_piece;
  }

  // arr[dict] (Pieces)
  let update_pieces = function(pieces_data) {
    pieces_ids = pieces_data.map(({ id }) => id);
    // Remove any pieces that have changed.
    let existing_ids = Object.keys(pieces);
    for (const existing_id of existing_ids) {
      if (!pieces_ids.includes(existing_id)) {
        console.log(`Found a piece present locally not present on the server. This shouldn't happen unless there's desync during multiplayer.`);
        remove_img(existing_id);
      }
    }

    // Upsert any pieces with changes.
    let old_ids = Object.keys(pieces);
    for (const new_piece of pieces_data) {
      let new_id = new_piece.id;
      if (!(old_ids.includes(new_id))) {
        console.log(`Found new piece not already present. This shouldn't happen after initial load, unless you've added some sort of graveyard mechanic: ${JSON.stringify(new_piece)}`);
        add_img(new_piece);
      } else {
        let old_piece = pieces[new_id];
        if (new_piece.row !== old_piece.row || new_piece.col !== old_piece.col) {
          console.log(`Found mismatched piece already present. This shouldn't happen unless movement got out of sync.\nNew: ${new_piece}\nOld: ${old_piece}`);
          remove_img(old_piece.id);
          add_img(new_piece);
        }
      }
    }
  };

  let update_turn = function(turn_data) {
    $("#active_color").text(turn_data);
  }

  let update_game = function(data) {
    update_pieces(data.pieces);
    update_turn(data.turn);
  }

  let initial_setup = function(data) {
    build_board(data.height, data.width);
    update_game(data);
  };

  let check_changes = function() {
    $.get('/state/' + game_id, function(data, status) {
      data = JSON.parse(data);
      update_game(data);
    });
  };

  $.get('/state/' + game_id, function(data, status) {
    console.log(`Status: ${status}, Data: ${data}`);
    data = JSON.parse(data);
    initial_setup(data);
  });

  change_interval = setInterval(check_changes, 1000);
});
