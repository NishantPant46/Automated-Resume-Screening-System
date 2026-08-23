from flask import Blueprint
from flask import render_template
from flask import flash
from flask_login import login_required

from app import db

from app.models.job_match_model import JobMatch
from app.models.selected_candidate_model import SelectedCandidate


selected_bp = Blueprint(
    "selected",
    __name__
)


# ---------------------------------------------
# Selection Threshold
# ---------------------------------------------

SELECTION_THRESHOLD = 50.0


# ---------------------------------------------
# Synchronize Selected Candidates
# ---------------------------------------------

def sync_selected_candidates():
    """
    Find all job matches with a score >= 50%
    and make sure they exist in the
    selected_candidates table.

    This also fixes old JobMatch records that
    were created before the SelectedCandidate
    insertion logic was added.
    """

    qualifying_matches = JobMatch.query.filter(
        JobMatch.similarity_score >= SELECTION_THRESHOLD
    ).all()

    added_count = 0

    for match in qualifying_matches:

        # Check whether this candidate/job
        # is already in selected_candidates.
        existing_selection = SelectedCandidate.query.filter_by(
            resume_id=match.resume_id,
            job_id=match.job_id
        ).first()

        if existing_selection:
            continue

        # Create selected candidate
        selected_candidate = SelectedCandidate(
            resume_id=match.resume_id,
            job_id=match.job_id
        )

        db.session.add(
            selected_candidate
        )

        added_count += 1

    # Save all newly selected candidates
    if added_count > 0:

        db.session.commit()

    return added_count


# ---------------------------------------------
# Selected Candidates
# ---------------------------------------------

@selected_bp.route("/selected")
@login_required
def selected_candidates():

    try:

        # -----------------------------------------
        # IMPORTANT:
        # Synchronize existing JobMatch records
        # into selected_candidates.
        # -----------------------------------------

        sync_selected_candidates()

        # -----------------------------------------
        # Now read directly from the
        # selected_candidates table.
        # -----------------------------------------

        selected_candidates = (
            SelectedCandidate.query
            .order_by(
                SelectedCandidate.selected_at.desc()
            )
            .all()
        )

        # -----------------------------------------
        # Send selected candidates to template
        # -----------------------------------------

        return render_template(
            "selected/selected_candidates.html",
            selected_candidates=selected_candidates
        )

    except Exception as e:

        # Roll back if database operation fails
        db.session.rollback()

        print(
            "Error loading selected candidates:",
            e
        )

        flash(
            "Unable to load selected candidates.",
            "danger"
        )

        return render_template(
            "selected/selected_candidates.html",
            selected_candidates=[]
        )