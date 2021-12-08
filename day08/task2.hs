import System.IO
import Data.List
import Data.Bits
import Data.Char
import Data.Maybe 


numberMap = [("abcefg", 0), ("cf", 1), ("acdeg", 2), ("acdfg", 3), ("bcdf", 4),
             ("abdfg", 5), ("abdefg", 6), ("acf", 7), ("abcdefg", 8),
             ("abcdfg", 9)]



realResult = do
        allContents <- readFile "data.txt"
        return $ (solve . convert) allContents


convert :: String -> [([String], [String])]
convert xs
  = map (\[xs1, xs2] -> (convert' xs1, convert' xs2)) xs''
  where
    xs'        = lines xs
    xs''       = map (splitOn '|') xs'
    convert':: String -> [String]
    convert' ys
      = map sort $ filter (/= "") $ words ys


splitOn :: (Eq a) => a -> [a] -> [[a]]
splitOn _ [] = []
splitOn delimiter str = 
    let (start, rest) = break (== delimiter) str
        (_, remain) = span (== delimiter) rest
     in start : splitOn delimiter remain



solve :: [([String], [String])] -> Int
solve xs
  = sum $ map solve' xs
  where
    solve' :: ([String], [String]) -> Int
    solve' (ys, zs)
      = foldl1 (\acc x -> acc * 10 + x) output
      where
        code = decode ys
        output = map (fromJust . (flip lookup code)) zs

decode :: [String] -> [(String, Int)]
decode xs
  = [(one, 1), (two, 2), (three, 3), (four, 4), (five, 5), (six, 6), (seven, 7),
     (eight, 8), (nine, 9), (zero, 0)]
  where
     [one]   = filter (\s -> length s == 2) xs
     [seven] = filter (\s -> length s == 3) xs
     [four]  = filter (\s -> length s == 4) xs
     [eight] = filter (\s -> length s == 7) xs
     len5    = filter (\s -> length s == 5) xs
     len6    = filter (\s -> length s == 6) xs
     [nine]  = filter (isSubsequenceOf four) len6
     [three] = filter (isSubsequenceOf seven) len5
     len5'   = len5 \\ [three]
     len6'   = len6 \\ [nine]
     [_a]    = seven \\ one
     [_b]    = nine \\ three
     [five]  = filter (elem _b) len5'
     [two]   = filter (notElem _b) len5'
     [zero]  = filter (isSubsequenceOf seven) len6'
     [six]   = len6' \\ [zero]




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
testInput = unlines ["be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
 "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
 "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |cg cg fdcagb cbg",
 "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |efabcd cedba gadfec cb",
 "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |gecf egdcabf bgf bfgea",
 "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |gebdcfa ecba ca fadegcb",
 "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |cefg dcbef fcge gbcadfe",
 "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |ed bcgafe cdgba cbgef",
 "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |gbdfcae bgc cg cgb",
 "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |fgae cfgab fg bagce"] 

testData = convert testInput
