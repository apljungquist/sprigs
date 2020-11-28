use std::collections::{HashMap, HashSet};
use std::fmt::Debug;
use std::iter::FromIterator;
use std::{cmp, hash};

use itertools::Itertools;

#[derive(Debug, Eq, PartialEq, PartialOrd, Ord, Copy, Clone)]
enum Side {
    Left,
    Right,
}

#[derive(Debug, Eq, PartialEq, PartialOrd, Ord)]
struct Endpoint<T: Ord, U: Ord> {
    when: U,
    side: Side,
    what: T,
}

fn endpoints<T: Copy + Ord, U: Ord>(intervals: Vec<(T, (U, U))>) -> Vec<Endpoint<T, U>> {
    let mut result = Vec::with_capacity(intervals.len() * 2);
    for (key, (left, right)) in intervals {
        result.push(Endpoint {
            when: left,
            side: Side::Left,
            what: key,
        });
        result.push(Endpoint {
            when: right,
            side: Side::Right,
            what: key,
        });
    }
    result
}

fn intervals<T: cmp::Eq + hash::Hash + Ord, U: Ord>(
    endpoints: Vec<Endpoint<T, U>>,
) -> HashMap<T, (U, U)> {
    let mut active = HashMap::new();
    let mut result = HashMap::new();
    for e in endpoints {
        match e.side {
            Side::Left => {
                active.insert(e.what, e.when);
            }
            Side::Right => {
                let left = active.remove(&e.what).unwrap();
                result.insert(e.what, (left, e.when));
            }
        }
    }
    result
}

pub fn intersecting_product<'a, T: Copy + cmp::Eq + hash::Hash + Ord, U: Ord>(
    factors: &'a Vec<HashMap<T, (U, U)>>,
) -> HashMap<Vec<&'a T>, (&'a U, &'a U)> {
    let mut indexed_intervals = Vec::new();
    for (i, factor) in factors.iter().enumerate() {
        for (key, (left, right)) in factor {
            indexed_intervals.push(((i, key), (left, right)))
        }
    }
    let mut indexed_endpoints = endpoints(indexed_intervals);
    indexed_endpoints.sort();
    let mut active = Vec::new();
    for _ in 0..factors.len() {
        active.push(HashSet::new());
    }
    let mut after = Vec::new();
    for e in indexed_endpoints {
        let (i, what) = e.what;
        match e.side {
            Side::Left => {
                active[i].insert(what);
            }
            Side::Right => (),
        }

        let mut tmp = active.to_vec();
        tmp[i] = HashSet::from_iter(vec![what]);

        for keys in tmp.iter().multi_cartesian_product() {
            let mut new = Vec::new();
            for key in keys {
                new.push(key.clone());
            }
            after.push(Endpoint {
                when: e.when,
                side: e.side,
                what: new,
            })
        }
        match e.side {
            Side::Left => (),
            Side::Right => {
                active[i].remove(&what);
            }
        }
    }
    intervals(after)
}

macro_rules! map (
    { $($key:expr => $value:expr),+ } => {
        {
            let mut mapping = HashMap::new();
            $(
                mapping.insert($key, $value);
            )+
            mapping
        }
     };
);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let before = vec![
            map! {0 => (1, 7)},
            map! {1 => (3, 9)},
            map! {2 => (0, 2), 3 => (0, 4)},
        ];
        let actual = intersecting_product(&before);
        let expected = map! {vec![&0, &1, &3] => (&3, &4)};
        assert_eq!(actual, expected);
    }
}
