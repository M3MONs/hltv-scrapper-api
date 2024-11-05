import subprocess

from classes import (
    JsonDataLoader as JDL,
    JsonFilePathGenerator as JFG,
    JsonOldDataCleaner as JODC,
    ConditionsChecker,
    ConditionFactory as CF,
)

BASE_DIR = "./hltv_scraper"
json_path = JFG(BASE_DIR)


def should_run_spider(json_name: str, hours: int = 1) -> bool:
    localization = json_path.generate(json_name)

    conditions = [CF.get("file_time"), CF.get("json_file_empty")]
    checker = ConditionsChecker(conditions)

    return checker.check(localization, hours)


def is_profile_link(filename: str, profile: str) -> bool:
    file = json_path.generate(filename)

    if not CF.get("file_exists").check(file):
        return False
    
    profiles = JDL().load(file)
    
    return profile in profiles


def get_profile_data(filename: str, profile: str) -> dict:
    file = json_path.generate(filename)
    profiles = JDL().load(file)
    return profiles[profile]


def run_spider(spider_name: str, json_name: str, args: str) -> None:
    path = json_path.generate(json_name)
    
    if CF.get("file_exists").check(path):
        JODC.clean(path)

    process = subprocess.Popen(
        ["scrapy", "crawl", spider_name] + args.split(),
        cwd=BASE_DIR,
    )
    process.wait()


def run_spider_and_get_data(spider: str, filename: str, spider_args: str) -> dict:
    json_loader = JDL()
    if should_run_spider(filename):
        run_spider(spider, filename, spider_args)
    return json_loader.load(json_path.generate(filename))
