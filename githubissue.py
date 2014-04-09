#!/usr/bin/env python

from github import Github
import re
import random
import sys
import subprocess
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('githubissuerc')
    if "Credentials" in config:
        credentials = config['Credentials']
    else:
        print("Error: Credentials could not be loaded.")
        sys.exit(1)
    if 'user' in credentials and 'password' in credentials:
        login = Github(credentials['user'], credentials['password'])
    githubissues(login.get_user())


class githubissues():
    def __init__(self, user):
        self.repo = user.get_repo("wget")
        self.repo_labels = self.repo.get_labels()
        repo_issues_page = self.repo.get_issues()
        self.repo_issues = list()
        self.local_issues = list()
        self.repo_issue_titles = list()
        self.repo_label_names = list()
        self.commit = subprocess.check_output(['git', 'rev-parse', '--short',
                                               'HEAD'])

        for label in self.repo_labels:
            self.repo_label_names.append(label.name)

        for issue in repo_issues_page:
            self.repo_issues.append(issue)
            self.repo_issue_titles.append(issue.title)

        self.populate_local_issues()
        self.update_issues()

    def populate_local_issues(self):
        with open("c2.txt") as warnings:
            for line in warnings:
                err_loc = re.search('^(.*?:[0-9]*?:[0-9]*?:)', line).group(1)
                title = re.search('warning:(.*?)\[', line).group(1)
                labels = re.search('\[-(.*?),(.*?)\]', line)
                issue_labels = [self._my_label(labels.group(1)),
                                self._my_label(labels.group(2))]
                issue_title = err_loc + title
                issue_body = line
                self.local_issues.append(my_issue(issue_title,
                                                  issue_body,
                                                  issue_labels))

    def _my_label(self, label_name):
        if label_name not in self.repo_label_names:
            label_color = "%06x" % random.randint(0, 0xFFFFFF)
            self.repo.create_label(label_name, label_color)
            self.repo_labels = self.repo.get_labels()
            self.repo_label_names.append(label_name)
        for label in self.repo_labels:
            if label.name == label_name:
                return label

    def update_issues(self):
        for loc_issue in self.local_issues:
            for net_issue in self.repo_issues:
                if loc_issue.title == net_issue.title:
                    self.repo_issues.remove(net_issue)
                    self.local_issues.remove(loc_issue)

        for loc_issue in self.local_issues:
            self.repo.create_issue(title=loc_issue.title, body=loc_issue.body,
                                   labels=loc_issue.labels)

        for net_issue in self.repo_issues:
            net_issue.create_comment("Fixed in commit " +
                                     self.commit.decode('utf-8'))
            net_issue.edit(state="closed")


class my_issue():
    def __init__(self, title, body, labels):
        self.title = title
        self.body = body
        self.labels = labels

if __name__ == '__main__':
    main()
