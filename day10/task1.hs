import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents


convert :: String -> [String]
convert xs
  = lines xs



splitOn :: (Eq a) => a -> [a] -> [[a]]
splitOn _ [] = []
splitOn delimiter str = 
    let (start, rest) = break (== delimiter) str
        (_, remain) = span (== delimiter) rest
     in start : splitOn delimiter remain



solve :: [String] -> Int
solve xs
  = foldl1 (+) $ map scoreLine xs


scoreLine :: String -> Int
scoreLine s
  = scoreLine' s []
  where
    scoreLine' :: String -> String -> Int
    scoreLine' [] ys
      = 0
    scoreLine' (']':xs) ('[':ys)
      = scoreLine' xs ys
    scoreLine' (')':xs) ('(':ys)
      = scoreLine' xs ys
    scoreLine' ('}':xs) ('{':ys)
      = scoreLine' xs ys
    scoreLine' ('>':xs) ('<':ys)
      = scoreLine' xs ys
    scoreLine' (x:xs) ys
      | elem x ['(', '[', '{', '<'] = scoreLine' xs (x:ys)
      | x == ')' = 3
      | x == ']' = 57
      | x == '}' = 1197
      | x == '>' = 25137
    


adjacentIndices :: Int -> Int -> Int -> Int -> [[Int]]
adjacentIndices i j h w
  = adjInd i j w ++ (map reverse $ adjInd j i h)
  where
    adjInd :: Int -> Int -> Int -> [[Int]]
    adjInd f v max
      | v == 0       = [below]
      | v == max - 1 = [above]
      | otherwise    = [above, below]
      where
        above = [f, v - 1]
        below = [f, v + 1]


splitBetween :: Int -> Int -> [a] -> ([a], [a], [a])
splitBetween i1 i2 xs
  = (first, second, third)
  where
    (first, remaining) = splitAt i1 xs
    (second, third)    = splitAt (i2 - i1 + 1) remaining


addToElem :: [Int] -> Int -> Int -> [Int]
addToElem xs i c 
  = xs' ++ ((x + c) : xs'')              
  where                                  
    (xs', x:xs'') = splitAt i xs


testInput :: String
testInput = unlines [
 "[({(<(())[]>[[{[]{<()<>>",
 "[(()[<>])]({[<{<<[]>>(",
 "{([(<{}[<>[]}>{[]{[(<()>",
 "(((({<>}<{<{<>}{[]{[]{}",
 "[[<[([]))<([[{}[[()]]]",
 "[{[{({}]{}}([{[{{{}}([]",
 "{<[[]]>}<{[{[{[]{()[[[]",
 "[<(<(<(<{}))><([]([]()",
 "<{([([[(<>()){}]>(<<{{",
 "<{([{{}}[<[[[<>{}]]]>[]]"]

testData = convert testInput
