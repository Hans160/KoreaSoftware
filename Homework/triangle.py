function leftInvertedTriangle(lines) {
  for (let i = lines; i >= 1; i--) {
    console.log("*".repeat(i));
  }
}

function rightTriangle(lines) {
  for (let i = 1; i <= lines; i++) {
    console.log(" ".repeat(lines - i) + "*".repeat(i));
  }
}

function rightInvertedTriangle(lines) {
  for (let i = lines; i >= 1; i--) {
    console.log(" ".repeat(lines - i) + "*".repeat(i));
  }
}

function isoscelesTriangle(lines) {
  for (let i = 1; i <= lines; i++) {
    console.log(" ".repeat(lines - i) + "*".repeat(2 * i - 1));
  }
}

function diamond(lines) {
  // 위쪽 삼각형
  for (let i = 1; i <= lines; i++) {
    console.log(" ".repeat(lines - i) + "*".repeat(2 * i - 1));
  }
  // 아래쪽 역삼각형
  for (let i = lines - 1; i >= 1; i--) {
    console.log(" ".repeat(lines - i) + "*".repeat(2 * i - 1));
  }
}