import System.IO
import System.Environment
import Text.Printf
import Data.Char  
-- An infinite stream of pseudorandom numbers in the range [0 .. 3].
mydiv :: Int -> Int -> Double
mydiv x y = (fromIntegral x) / (fromIntegral y)
 
pseudo_random :: [Int]
pseudo_random =
    let f :: Integer -> Integer
        f x = (6364136223846793005 * x + 1442695040888963407) `mod` (2 ^ 64)
        stream = iterate f 1
    in map (\n -> fromIntegral (n `div` (2 ^ 62))) stream

step :: (Int,Int) -> Int -> (Int,Int)
step (x,y) i = if (i == 0) then (x,y+1)
               else if i == 1 then (x,y-1)
               else if i == 2 then (x-1,y)
               else (x+1,y) 

fall :: Int -> Int -> (Int,Int) -> Bool
fall given i (x,y) = if fst(step (x,y) i) > given ||
  snd(step(x,y) i) > given then True
  else if fst(step (x,y) i) < -given ||
  snd(step(x,y) i) < -given then True else False

back_to_sleep :: Int -> (Int,Int) -> Bool
back_to_sleep i (x,y) = if (step (x,y) i == (0,0)) then True else False

walk :: Int -> (Int,Int) -> (Int, [Int]) -> (Int, [Int])
walk given (x,y) (suc, (l:ls)) = if fall given l (x,y) == True then (suc, ls) else if back_to_sleep l (x,y) == True then (succ (suc), ls) else walk given (step (x,y) l) (suc, ls)

survival :: Int -> Int -> String
survival suc pos = printf "%.1f" ((mydiv suc pos) *100.0)

whole_walk :: Int -> Int -> (Int, [Int]) -> [(Int, [Int])]
whole_walk _ _ (_,[]) = []
whole_walk _ 0 (_,_) = []
whole_walk size trial (suc, ls) = walk size (0,0) (suc, ls) : whole_walk size (trial -1) (walk size (0,0) (suc, ls) )

whole_walk' :: Int -> Int -> Int
whole_walk' size trial = fst (last (whole_walk size trial (0, pseudo_random)))

main = do 
    size <- getLine
    trial <- getLine 
    let x = read size :: Int
    let y = read trial :: Int
    putStrLn $ "survived " ++ (survival (whole_walk' x y) y) ++ "% (" ++ (show (whole_walk' x y)) ++ " / " ++ trial ++")"
