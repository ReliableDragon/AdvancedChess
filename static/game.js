// piece_data: img_id
var pieces = {};
var highlighted_ids = [];
var highlighted_piece = null;

$(document).ready(function() {

  let highlight_moves = function(piece_data) {
    return function() {
      console.log(piece_data);
      let piece_id = String(piece_data.row) + String(piece_data.column);
      if (highlighted_piece != null) {
        if (highlighted_piece == piece_id) {
          for (const id of highlighted_ids) {
            $(`#${id}`).remove();
          }
          highlighted_ids = [];
          highlighted_piece = null;
          return;
        } else {
          return;
        }
      }

      // Nothing is already highlighted, so show moves.
      highlighted_piece = piece_id;
      for (const square of piece_data.valid_moves) {
        let x = square[0];
        let y = square[1];
        let target_id = String(x) + String(y);
        let highlight = $(`<div class=valid_move id="highlight${target_id}"></div>`);
        $(`#square${target_id}`).append(highlight);
        highlighted_ids.push(`highlight${target_id}`);
      }

      if (!("valid_attacks" in piece_data)) {
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

  let update_pieces = function(pieces_data) {
    // Remove any pieces that have changed.
    for (const [piece, img_id] of Object.entries(pieces)) {
      console.log(`Processing existing piece ${piece}.`);
      if (!pieces_data.includes(piece)) {
        console.log(`Removing piece ${piece}.`)
        $(`#${img_id}`).remove();
      }
    }

    // Add any pieces with changes.
    for (const piece of pieces_data) {
      if (!(String(piece) in pieces)) {
        console.log(`Adding piece ${piece}.`)
        id = String(piece.type) + String(piece.row) + String(piece.column);
        let img = $(`<img id=${id} class="piece" src=/static/imgs/${piece.type}.png alt=${piece.type}>`);
        let square = $(`#square${piece.row}${piece.column}`);
        square.append(img);
        square.click(highlight_moves(piece));
        pieces[JSON.stringify(piece)] = id;
      }
    }
  };

  let initial_setup = function(data) {
    build_board(data.height, data.width);
    console.log(`Data: ${data}`);
    update_pieces(data.pieces);
  };

  $.get('/state/24601', function(data, status) {
    console.log(`Status: ${status}, Data: ${data}`);
    data = JSON.parse(data);
    initial_setup(data);
  });
});
