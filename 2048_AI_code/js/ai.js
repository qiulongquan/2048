function AI(grid) {
  // grid是一个实例化对象 里面包括一个2维数组和参数
  this.grid = grid;
  // grid是当前的16个cell里面的数字列表  and playerTurn
  // document.write("grid="+grid);
}

// 格局评价---启发指标采用了加权策略
// static evaluation function
AI.prototype.eval = function() {
  // emptyCells 这个是当前为0的cell的个数
  var emptyCells = this.grid.availableCells().length;
  // document.write("emptyCells="+emptyCells);
  // console.log("emptyCells= ",emptyCells);

  var smoothWeight = 0.1,
      //monoWeight   = 0.0,
      //islandWeight = 0.0,
      mono2Weight  = 1.0,
      emptyWeight  = 2.7,
      maxWeight    = 1.0;

  // a=this.grid.smoothness();
  // b=this.grid.monotonicity2();
  // c=Math.log(emptyCells);
  // d=this.grid.maxValue();
  //
  // res=a*smoothWeight+b*mono2Weight+c*emptyWeight+d*maxWeight;
  // console.log("result=%f",res);
  // 最后算出一个格局评价的值然后返回
  return this.grid.smoothness() * smoothWeight
       //+ this.grid.monotonicity() * monoWeight
       //- this.grid.islands() * islandWeight
       + this.grid.monotonicity2() * mono2Weight
       + Math.log(emptyCells) * emptyWeight
       + this.grid.maxValue() * maxWeight;   // maxValue代表当前方格中的最大数字
};

// alpha-beta depth first search
AI.prototype.search = function(depth, alpha, beta, positions, cutoffs) {
  var bestScore;
  var bestMove = -1;
  var result;

  // the maxing player
  if (this.grid.playerTurn) {
    bestScore = alpha;
    for (var direction in [0, 1, 2, 3]) {
      // newGrid包括playerTurn=true和一个最新的2维数组状态
      var newGrid = this.grid.clone();
      if (newGrid.move(direction).moved) {
        positions++;
        if (newGrid.isWin()) {
          return { move: direction, score: 10000, positions: positions, cutoffs: cutoffs };
        }
        var newAI = new AI(newGrid);

        if (depth == 0) {
          result = { move: direction, score: newAI.eval() };
        } else {
          result = newAI.search(depth-1, bestScore, beta, positions, cutoffs);
          if (result.score > 9900) { // win
            result.score--; // to slightly penalize higher depth from win
          }
          positions = result.positions;
          cutoffs = result.cutoffs;
        }
        var result_str = JSON.stringify(result);
        console.log("result返回值 self.grid.playerTurn=True ",result_str);

        if (result.score > bestScore) {
          bestScore = result.score;
          bestMove = direction;
        }
        if (bestScore > beta) {
          cutoffs++;
          var result_str1 = JSON.stringify({ move: bestMove, score: beta, positions: positions, cutoffs: cutoffs });
          console.log("bestScore > beta cutoff加1 剪切掉 self.grid.playerTurn=True ",result_str1);
          return { move: bestMove, score: beta, positions: positions, cutoffs: cutoffs };
        }
      }
    }
  }

  else { // computer's turn, we'll do heavy pruning to keep the branching factor low
    bestScore = beta;
    console.log("------self.grid.playerTurn=False-------")
    // try a 2 and 4 in each cell and measure how annoying it is
    // with metrics from eval
    var candidates = [];
    var cells = this.grid.availableCells();
    var scores = { 2: [], 4: [] };
    for (var value in scores) {
      for (var i in cells) {
        scores[value].push(null);
        // 从cells里面拿出一个空值的坐标给cell 为了去创建tile实例
        var cell = cells[i];
        // 建立tile 创建一个tile实例  里面包括数值和坐标
        var tile = new Tile(cell, parseInt(value, 10));
        // 刚才建立的tile插入到insertTile里面去
        this.grid.insertTile(tile);
        // 计算evaluation放入scores字典里面
        scores[value][i] = -this.grid.smoothness() + this.grid.islands();
        // 最后删掉刚才插入的cell
        this.grid.removeTile(cell);
      }
    }

    // now just pick out the most annoying moves
    var maxScore = Math.max(Math.max.apply(null, scores[2]), Math.max.apply(null, scores[4]));
    for (var value in scores) { // 2 and 4
      for (var i=0; i<scores[value].length; i++) {
        if (scores[value][i] == maxScore) {
          // 创建候选者列表  符合maxscore最大值的坐标和数字进入到候选者列表中
          candidates.push( { position: cells[i], value: parseInt(value, 10) } );
        }
      }
    }

    // search on each candidate
    for (var i=0; i<candidates.length; i++) {
      var position = candidates[i].position;
      var value = candidates[i].value;
      var newGrid = this.grid.clone();
      var tile = new Tile(position, value);
      newGrid.insertTile(tile);
      newGrid.playerTurn = true;
      positions++;
      newAI = new AI(newGrid);
      result = newAI.search(depth, alpha, bestScore, positions, cutoffs);
      positions = result.positions;
      cutoffs = result.cutoffs;

      if (result.score < bestScore) {
        bestScore = result.score;
      }
      if (bestScore < alpha) {
        cutoffs++;
        var result_str2 = JSON.stringify({ move: null, score: alpha, positions: positions, cutoffs: cutoffs });
        console.log("self.grid.playerTurn=False ",result_str2);
        return { move: null, score: alpha, positions: positions, cutoffs: cutoffs };
      }
    }
  }

  return { move: bestMove, score: bestScore, positions: positions, cutoffs: cutoffs };
};

// performs a search and returns the best move
AI.prototype.getBest = function() {
  return this.iterativeDeep();
};

// performs iterative deepening over the alpha-beta search
AI.prototype.iterativeDeep = function() {
  var start = (new Date()).getTime();
  var depth = 0;
  var best;
  console.log("本次search开始");
  // window.alert("本次search开始");
  do {
    var newBest = this.search(depth, -10000, 10000, 0 ,0);
    var str1 = JSON.stringify(newBest);
    console.log("newBest_%d=",depth,str1);
    // window.alert(str1);

    if (newBest.move == -1) {
      break;
    } else {
      best = newBest;
    }
    depth++;
  } while ( (new Date()).getTime() - start < minSearchTime);
  console.log("本次search结束");
  // window.alert("本次search结束");
  var best_str = JSON.stringify(best);
  console.log("best=",best_str);
  return best
};

AI.prototype.translate = function(move) {
 return {
    0: 'up',
    1: 'right',
    2: 'down',
    3: 'left'
  }[move];
};
