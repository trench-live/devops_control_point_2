const CONFIG = {
    labels: {
        passed: "${{ vars.labels.test_passed }}",
        failed: "${{ vars.labels.test_failed }}"
    }
};

/**
 * Main reporting function
 * @param {Object} params - { github, context, status }
 */
module.exports.report = async ({ github, context, status }) => {
    if (context.eventName !== 'pull_request') return;

    // Cleanup old labels
    const { data: labels } = await github.rest.issues.listLabelsOnIssue({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo
    });

    await Promise.all(
        labels
            .filter(l => l.name.startsWith('test-'))
            .map(l => github.rest.issues.removeLabel({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                name: l.name
            }))
    );

    // Add new label
    await github.rest.issues.addLabels({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        labels: [CONFIG.labels[status]]
    });

    // Add comment
    const message = status === 'passed'
        ? "✅ All tests passed successfully"
        : "❌ Test failures detected";

    await github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: message
    });
};