
var pieces = {}; // id: dict(piece) + img_id
var highlighted_ids = [];
var highlighted_piece_id = null;
var change_interval;
var turn = 'white';

$(document).ready(function() {

  let clear_highlights = function() {
    console.log(`Clearing highlights: ${highlighted_ids}`);
    for (const id of highlighted_ids) {
        console.log(`Clearing highlight: ${id}`);
        console.log($(`#${id}`));
        $(`#${id}`).prop("onclick", null).off("click");
        $(`#${id}`).remove();
      // endturnbutton.prop("onclick", null);
    }
    highlighted_ids = [];
    highlighted_piece_id = null;
  }

  let make_move = function(piece_id, row, col) {
    return function() {
      disable_turn_buttons();
      let move_obj = {
        'game_id': game_id,
        'move_data': {
          'piece_id': piece_id,
          'row': row,
          'col': col
        }
      };
      let move = JSON.stringify(move_obj);
      $.ajax({
        url: '/move/',
        type: 'POST',
        data: move,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false,
        success: function(json_data) {
            // console.log(json_data);
            // let data = JSON.parse(msg);
            update_game(json_data);
            $('#gameboard').click(highlight_moves);
        }
      });
    }
  };

  let disable_turn_buttons = function() {
      let undobutton = $("#undobutton");
      let endturnbutton = $("#endturnbutton");
      undobutton.addClass('disabled');
      endturnbutton.addClass('disabled');
      undobutton.prop("onclick", null).off("click");
      endturnbutton.prop("onclick", null).off("click");
  };

  let undo = function(piece_id, row, col, captured_piece) {
    return function() {
      piece = pieces[piece_id];
      piece.row = row;
      piece.col = col;
      if (captured_piece) {
        pieces[captured_piece.id] = captured_piece;
        draw_piece(captured_piece);
      }
      remove_img(piece_id);
      draw_piece(piece);
      disable_turn_buttons();
      $('#gameboard').click(highlight_moves);
    };
  };

  let get_piece_by_coords = function(row, col) {
    // Find piece at row/col.
    let piece_list = Object.values(pieces);
    let piece_data = Object.values(piece_list).find(obj => { return obj.row === row && obj.col === col });
    // This typically happens when the old square is clicked on during a prospective move.
    if (!piece_data) {
      return null;
    }
    return piece_data;
  }

  let preview_move = function(piece_id, row, col) {
    return function() {
      console.log("Previewing move!");
      let moving_piece_id = piece_id;
      let moving_piece = pieces[moving_piece_id];

      clear_highlights();
      $('#gameboard').prop("onclick", null).off("click");
      // console.log(`${$('#gameboard').
      remove_img(moving_piece_id);

      // Check for captures
      let captured_piece = get_piece_by_coords(row, col);
      if (captured_piece) {
        remove_img(captured_piece.id);
        delete pieces[captured_piece.id];
      }

      let old_row = moving_piece.row;
      let old_col = moving_piece.col;
      moving_piece.row = row;
      moving_piece.col = col;

      draw_img(moving_piece.id, moving_piece.icon, moving_piece.row, moving_piece.col);

      let undobutton = $("#undobutton");
      let endturnbutton = $("#endturnbutton");
      undobutton.removeClass('disabled');
      endturnbutton.removeClass('disabled');
      undobutton.click(undo(moving_piece.id, old_row, old_col, captured_piece));
      endturnbutton.click(make_move(moving_piece.id, row, col));
    }
  };


  let highlight_moves = function(e) {
    // Extract row/col from ID of square that triggered the event.
    let dom_path = e.originalEvent.path;
    let square_dom = dom_path.find(obj => { return obj.id.substr(0, 6) === "square" })
    // Short-circuit clicks on non-pieces.
    if (!square_dom) {
      return;
    }
    let parts = square_dom.id.split("_");
    let row = Number(parts[1]);
    let col = Number(parts[2]);

    // Find piece at row/col.
    let piece_data = get_piece_by_coords(row, col);
    // This typically happens when the old square is clicked on during a prospective move.
    if (!piece_data) {
      return;
    }

    if (highlighted_piece_id != null) {
      if (highlighted_piece_id === piece_data.id) {
        clear_highlights();
        return;
      } else {
        return;
      }
    }

    if (piece_data.color !== turn) {
      return;
    }

    console.log("Doing some highlighting!")
    // Nothing is already highlighted, so show moves.
    highlighted_piece_id = piece_data.id;
    let piece_coord = String(piece_data.row) + "_" + String(piece_data.col);
    let self_highlight_id = `highlight${piece_data.id}`;
    $(`#square_${piece_coord}`).append(`<div class=active_piece id="${self_highlight_id}"></div>`);
    highlighted_ids.push(self_highlight_id);

    console.log(`Valid moves: ${piece_data.valid_moves}`)
    for (const square of piece_data.valid_moves) {
      let row = square[0];
      let col = square[1];
      let target_id = String(row) + "_" + String(col);
      let highlight = $(`<div class=valid_move id="highlight${target_id}"></div>`);
      highlight.click(preview_move(highlighted_piece_id, row, col));
      $(`#square_${target_id}`).append(highlight);
      highlighted_ids.push(`highlight${target_id}`);
    }

    if (!("valid_attacks" in piece_data) || !piece_data.valid_attacks) {
      return;
    }
    for (const square of piece_data.valid_attacks) {
      let row = square[0];
      let col = square[1];
      let target_id = String(row) + "_" + String(col);
      let highlight = $(`<div class=valid_attack id="highlight${target_id}"></div>`);
      $(`#square_${target_id}`).append(highlight);
      highlighted_ids.push(`highlight${target_id}`);
    }
  };

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
        let square = $(`#${color}_root`).clone().attr('id', `square_${i}_${j}`);
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
    delete piece.img_id;
  }

  let draw_img = function(piece_id, icon, row, col) {
    // Backup check, should already be removed.
    if (pieces[piece_id] && 'img_id' in pieces[piece_id]) {
      remove_img(piece_id);
    }

    let img_id = "img_" + piece_id;
    let img = $(`<img id=${img_id} class="piece" src=/static/imgs/${icon}.png alt=${icon}>`);
    let square = $(`#square_${row}_${col}`);
    square.append(img);
    pieces[piece_id].img_id = img_id;
  };

  let draw_piece = function(piece) {
    draw_img(piece.id, piece.icon, piece.row, piece.col);
  }

  // dict{int: dict} (Dict of ID to Pieces)
  let update_pieces = function(pieces_data) {
    pieces_ids = Object.keys(pieces_data);
    // Remove any pieces that have changed.
    let existing_ids = Object.keys(pieces);
    for (const existing_id of existing_ids) {
      if (!pieces_ids.includes(existing_id)) {
        console.log(`Found a piece present locally not present on the server. This shouldn't happen unless there's desync during multiplayer.`);
        remove_img(existing_id);
        delete pieces[existing_id];
      }
    }

    // Upsert any pieces with changes.
    let old_ids = Object.keys(pieces);
    for (const [new_id, new_piece] of Object.entries(pieces_data)) {
      // let new_id = new_piece.id;
      if (!(old_ids.includes(new_id))) {
        console.log(`Found new piece not already present. This shouldn't happen after initial load, unless you've added some sort of graveyard mechanic: ${JSON.stringify(new_piece)}`);
        pieces[new_id] = new_piece;
        draw_piece(new_piece);
      } else {
        let stored_piece = pieces[new_id];
        stored_piece.valid_moves = new_piece.valid_moves;
        if (new_piece.row !== stored_piece.row || new_piece.col !== stored_piece.col) {
          console.log(`Found mismatched piece already present. This shouldn't happen unless movement got out of sync.\nNew: ${new_piece}\nOld: ${stored_piece}`);
          remove_img(stored_piece.id);
          pieces[new_id] = new_piece;
          draw_piece(new_piece);
        }
      }
    }
  };

  let update_turn = function(turn_data) {
    $("#active_color").text(turn_data);
    turn = turn_data;
  }

  let update_game = function(data) {
    console.log(data)
    update_pieces(data.pieces);
    update_turn(data.turn);
  }

  let initial_setup = function(data) {
    build_board(data.height, data.width);
    update_game(data);
    $('#gameboard').click(highlight_moves);
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

  // No need to check changes until multiplayer is added. Will need to fix
  // conflict between tentative moves and server data, probably by not polling
  // while it's the player's turn.
  // change_interval = setInterval(check_changes, 1000);
});
